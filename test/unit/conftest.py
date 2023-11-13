import pytest
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from password_manager.src.core.database_manager import DatabaseManager


@pytest.fixture(scope="session")
def key() -> bytes:
    """Random Encryptation key"""
    salt = os.urandom(16)
    password = b"password"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))


@pytest.fixture(scope="session")
def database_manager(tmp_path_factory: pytest.TempPathFactory) -> DatabaseManager:
    """Create Database Manager Object"""
    filepath = tmp_path_factory.mktemp("data") / "database.db"
    return DatabaseManager(filepath)
