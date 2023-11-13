from dataclasses import (dataclass, field)
from string import (digits, ascii_letters)
from random import choices
from .note import Note

CHARACTERS = digits + ascii_letters + "#$%&?@"
PASSWORD_LENGTH = 16


@dataclass
class Service:
    """A class that represent a web service login data."""

    id: int = field(default=-1)
    domain: str = field(default='')
    user: str = field(default='')
    password_encrypted: str = field(default='')
    password: str = field(default='')
    notes: list[Note] = field(default_factory=list[Note])
    is_encrypted: bool = field(default=True)

    def sql_repr(self) -> tuple[str]:
        return (self.domain, self.user, self.password_encrypted)

    def setRandomStrongPassword(self) -> None:
        self.password = "".join(choices(CHARACTERS, k=PASSWORD_LENGTH))