import pytest
from password_manager.src.core.database_manager import DatabaseManager
from password_manager.src.core.service import Service


@pytest.fixture
def new_service() -> Service:
    return Service(
        domain="domain.com",
        user="user",
        password="password",
    )


def test_add_service(database_manager: DatabaseManager, new_service: Service):
    result = database_manager.add_service(new_service)
    services = database_manager.services_encrypted()
    assert result == True
    assert services == [new_service]
