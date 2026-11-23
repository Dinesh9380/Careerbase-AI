import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, get_db
from app.core.security import get_password_hash
from app.models.models import User, StudentProfile

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client
