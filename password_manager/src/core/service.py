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
    password_token: str = field(default='')
    password: str = field(default='')
    notes: list[Note] = field(default_factory=list[Note])
    is_encrypted: bool = field(default=True)

    def sql_repr(self) -> tuple[str]:
        return (self.domain, self.user, self.password_token)

    def setRandomStrongPassword(self) -> None:
        self.password = "".join(choices(CHARACTERS, k=PASSWORD_LENGTH))

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id
