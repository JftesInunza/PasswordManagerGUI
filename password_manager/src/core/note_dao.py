import sqlite3
from .tables import Tables
from .note import Note


class NoteDAO:
    cursor: sqlite3.Cursor

    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self.cursor = cursor

    def init_table(self) -> None:
        """Initialize database file and tables."""
        query = f"""
            CREATE TABLE IF NOT EXISTS {Tables.NOTES} (
                id integer PRIMARY KEY,
                title text,
                content_token text,
                service_id integer
            );
        """
        self.cursor.execute(query)

    def add_note_in_service(self, service_id: int, note: Note) -> None:
        """Add a new service to the database after data encryptation."""
        query = f"""
            INSERT INTO {Tables.NOTES} (title, content_token, service_id) VALUES (?,?,?);
        """
        note.service_id = service_id
        self.cursor.execute(query, note.sql_repr())
        note.id = self.cursor.lastrowid

    def remove_note(self, id: int) -> None:
        """remove service at given id."""
        query = f"""DELETE FROM {Tables.NOTES} WHERE id = {id};"""
        self.cursor.execute(query)

    def remove_notes_for_service(self, service_id: int) -> None:
        """Remove all notes of the given service id"""
        query = f"""DELETE FROM {Tables.NOTES}
            WHERE service_id = {service_id};"""
        self.cursor.execute(query)

    def notes(self, service_id: int) -> list[Note]:
        """Load all services in database."""
        query = f"""SELECT * FROM {Tables.NOTES}
            WHERE service_id = {service_id};"""
        self.cursor.execute(query)
        return [Note(*sql) for sql in self.cursor.fetchall()]
