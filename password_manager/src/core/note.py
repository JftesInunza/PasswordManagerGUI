from dataclasses import dataclass, field


@dataclass
class Note:
    id: int = field(default=-1)
    title: str = field(default="")
    content_encrypted: str = field(default="")
    content: str = field(default="")

    def sql_repr(self, serviceId: int = None) -> list[str]:
        sql = [self.title, self.content_encrypted]
        if serviceId:
            sql.append(serviceId)
        return sql
