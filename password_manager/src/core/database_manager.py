from .singleton import SingletonMeta
from .service import Service
from .note import Note
from .database_access import DatabaseAccess
from . import service_daf
from . import note_daf



class DatabaseManager(metaclass=SingletonMeta):
    """A class that manage the storage of the Web Service's
    login data into a sql database."""

    dao: DatabaseAccess

    def __init__(self, dao: DatabaseAccess) -> None:
        self.dao = dao
        dao.open()
        note_daf.init_note_table(dao=self.dao)
        service_daf.init_service_table(dao=self.dao)

    def add_service(self, service: Service) -> bool:
        return service_daf.add_service(service, dao=self.dao)
            
    def add_note(self, serviceId: int, note: Note) -> bool:
        return note_daf.add_note(serviceId, note, dao=self.dao)

    def update_service(self, service: Service) -> bool:
        return service_daf.update_service(service, dao=self.dao)
        
    def update_note(self, note: Note) -> bool:
        return note_daf.update_note(note, dao=self.dao)

    def remove_service(self, id: str) -> bool:
        note_daf.remove_all_notes(id, dao=self.dao)
        return service_daf.remove_service(id, dao=self.dao)
    
    def remove_note(self, id: str) -> bool:
        return note_daf.remove_note(id, dao=self.dao)

    def services_encrypted(self) -> list[Service]:
        return service_daf.services(dao=self.dao)
        
    def services_decrypted(self) -> list[Service]:
        services = self.services_encrypted()
        for service in services:
            # service.decrypt(self.dao.key)
            pass
        return services
