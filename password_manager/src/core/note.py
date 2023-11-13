from dataclasses import dataclass, field
from typing import Any


@dataclass
class Note:
    id: int = field(default=-1)
    title: str = field(default="")
    content_token: str = field(default="")
    service_id: int = field(default=-1)
    content: str = field(default="")

    def sql_repr(self) -> tuple[Any]:
        return (self.title, self.content_token, self.service_id)

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id
