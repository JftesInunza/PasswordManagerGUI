from .database_access import DatabaseAccess, Tables, query_call
from .service import Service
from . import note_daf


@query_call
def init_service_table(dao: DatabaseAccess = None) -> bool:
    """Initialize database file and tables."""
    query = f"""
        CREATE TABLE IF NOT EXISTS {Tables.SERVICES} (
            id integer PRIMARY KEY,
            domain text,
            user text,
            pass text
            );
    """
    dao.execute(query)
    return True


@query_call
def add_service(service: Service, dao: DatabaseAccess = None) -> bool:
    """Add a new service to the database after data encryptation."""
    query = f"""
        INSERT INTO {Tables.SERVICES} (domain, user, pass) VALUES (?,?,?);
    """
    dao.execute(query, service.sql_repr())
    service.id = dao.last_id()
    success = [note_daf.add_note(service.id, note, dao=dao) for note in service.notes]
    return all(success)


@query_call
def update_service(service: Service, dao: DatabaseAccess = None) -> bool:
    """Update the service given."""
    query = f"""
        UPDATE {Tables.SERVICES} SET domain = ?, user = ?, pass = ? 
        WHERE id = {service.id};
    """
    dao.execute(query, service.sql_repr())
    return True


@query_call
def remove_service(id: str, dao: DatabaseAccess = None) -> bool:
    """remove service at given id."""
    query = f"""DELETE FROM {Tables.SERVICES} WHERE id = {id};"""
    dao.execute(query)
    note_daf.remove_all_notes(id, dao=dao)
    return True


@query_call
def services(dao: DatabaseAccess = None) -> list[Service]:
    """Load all services in database."""
    query = f"""SELECT * FROM {Tables.SERVICES};"""
    dao.execute(query)
    services = []
    for fetched in dao.fetchall():
        service = Service(*fetched)
        service.notes = note_daf.notes(service.id, dao)
        services.append(service)

    return services
