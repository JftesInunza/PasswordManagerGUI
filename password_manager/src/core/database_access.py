import sqlite3
from typing import Callable
from pathlib import Path
from dataclasses import dataclass, field


class Tables:
    NOTES = "notes"
    SERVICES = "services"


@dataclass
class DatabaseAccess:
    filepath: Path
    trace: bool = field(default=False)
    conn: sqlite3.Connection = field(init=False)
    cursor: sqlite3.Cursor = field(init=False)

    def open(self) -> None:
        self.conn = sqlite3.connect(self.filepath)
        if self.trace:
            self.conn.set_trace_callback(print)
        self.cursor = self.conn.cursor()

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def commit(self) -> None:
        if self.conn:
            self.conn.commit()

    def rollback(self) -> None:
        if self.conn:
            self.conn.rollback()

    def execute(self, sql: str, parameters: tuple[str] = ()) -> sqlite3.Cursor | None:
        if self.cursor:
            return self.cursor.execute(sql, parameters)
        return None

    def fetchall(self) -> list[str]:
        if self.cursor:
            return self.cursor.fetchall()
        return []

    def last_id(self) -> int:
        if self.cursor:
            return self.cursor.lastrowid
        return -1


def query_call(query: Callable) -> Callable:
    def inner(*args, **kwargs) -> bool:
        dao: DatabaseAccess = kwargs.get("dao")
        result = None

        try:
            result = query(*args, **kwargs)
            dao.commit()
        except sqlite3.Error as err:
            dao.rollback()
            dao.close()
            print(err)

        return False if result is None else result

    return inner
