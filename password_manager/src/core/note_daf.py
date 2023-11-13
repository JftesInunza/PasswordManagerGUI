from .database_access import DatabaseAccess, Tables, query_call
from .note import Note


@query_call
def init_note_table(dao: DatabaseAccess = None) -> bool:
    """Initialize database file and tables."""
    query = f"""
        CREATE TABLE IF NOT EXISTS {Tables.NOTES} (
            id integer PRIMARY KEY,
            title text,
            content text,
            serviceId integer,
        );
    """
    dao.execute(query)
    return True


@query_call
def add_note(serviceId: int, note: Note, dao: DatabaseAccess = None) -> bool:
    """Add a new service to the database after data encryptation."""
    query = f"""
        INSERT INTO {Tables.NOTES} (title, content, serviceId) VALUES (?,?,?);
    """
    dao.execute(query, note.sql_repr(serviceId))
    note.id = dao.last_id()
    return True


@query_call
def update_note(note: Note, dao: DatabaseAccess = None) -> bool:
    """Update the service given."""
    query = f"""
        UPDATE {Tables.NOTES} SET title = ?, content = ?
        WHERE id = {note.id};
    """
    dao.execute(query, note.sql_repr())
    return True


@query_call
def remove_note(id: int, dao: DatabaseAccess = None) -> bool:
    """remove service at given id."""
    query = f"""DELETE FROM {Tables.NOTES} WHERE id = {id};"""
    dao.execute(query)
    return True


@query_call
def remove_all_notes(serviceId: int, dao: DatabaseAccess = None) -> bool:
    """Remove all notes of the given service id"""
    query = f"""DELETE FROM {Tables.NOTES} WHERE serviceId = {serviceId};"""
    dao.execute(query)
    return True


@query_call
def notes(serviceId: int, dao: DatabaseAccess = None) -> list[Note]:
    """Load all services in database."""
    query = f"""SELECT * FROM {Tables.NOTES} WHERE serviceId = {serviceId};"""
    dao.execute(query)
    return [Note(*sql) for sql in dao.fetchall()]
