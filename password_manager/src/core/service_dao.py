import sqlite3
from .tables import Tables
from .service import Service


class ServiceDAO:
    cursor: sqlite3.Cursor

    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self.cursor = cursor

    def init_table(self) -> bool:
        """Initialize database file and tables."""
        query = f"""
            CREATE TABLE IF NOT EXISTS {Tables.SERVICES} (
                id integer PRIMARY KEY,
                domain text,
                user text,
                password_token text
                );
        """
        self.cursor.execute(query)
        return True

    def add_service(self, service: Service) -> None:
        """Add a new service to the database after data encryptation."""
        query = f"""
            INSERT INTO {Tables.SERVICES} (domain, user, password_token) VALUES (?,?,?);
        """
        self.cursor.execute(query, service.sql_repr())
        service.id = self.cursor.lastrowid

    def update_service(self, service: Service) -> None:
        """Update the service given."""
        query = f"""
            UPDATE {Tables.SERVICES} SET domain = ?, user = ?, password_token = ?
            WHERE id = {service.id};
        """
        self.cursor.execute(query, service.sql_repr())

    def remove_service(self, id: int) -> None:
        """remove service at given id."""
        query = f"""DELETE FROM {Tables.SERVICES} WHERE id = {id};"""
        self.cursor.execute(query)

    def services(self) -> list[Service]:
        """Load all services in database."""
        query = f"""SELECT * FROM {Tables.SERVICES};"""
        self.cursor.execute(query)
        return [Service(*fetched) for fetched in self.cursor.fetchall()]
