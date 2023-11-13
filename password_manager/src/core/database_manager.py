import sqlite3
from pathlib import Path
from .singleton import SingletonMeta
from .service_dao import Service, ServiceDAO
from .note_dao import Note, NoteDAO


class DatabaseManager(metaclass=SingletonMeta):
    """A class that manage the storage of the Web Service's
    login data into a sql database."""

    conn: sqlite3.Connection
    cursor: sqlite3.Cursor
    service_dao: ServiceDAO
    note_dao: NoteDAO

    def __init__(self, filepath: Path) -> None:
        self.conn = sqlite3.connect(filepath)
        self.cursor = self.conn.cursor()
        self.service_dao = ServiceDAO(self.cursor)
        self.note_dao = NoteDAO(self.cursor)

        self.service_dao.init_table()
        self.note_dao.init_table()

    def add_service(self, service: Service) -> None:
        return self.service_dao.add_service(service)

    def update_service(self, service: Service) -> None:
        return self.service_dao.update_service(service)

    def remove_service(self, id: int) -> None:
        return self.service_dao.remove_service(id)

    def services(self) -> list[Service]:
        return self.service_dao.services()

    def add_note_in_service(self, service_id: int, note: Note) -> None:
        return self.note_dao.add_note_in_service(service_id, note)

    def remove_note(self, id: int) -> None:
        return self.note_dao.remove_note(id)

    def remove_notes_for_service(self, service_id: int) -> None:
        return self.note_dao.remove_notes_for_service(service_id)

    def notes(self, service_id: int) -> list[Note]:
        return self.note_dao.notes(service_id)
