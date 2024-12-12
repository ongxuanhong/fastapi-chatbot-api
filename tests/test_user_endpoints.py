import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.db.database import Base, get_db

# Setup test database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the database dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create tables for the test database
Base.metadata.create_all(bind=engine)

# Test client
client = TestClient(app)


@pytest.fixture(scope="function")
def clear_database():
    # Clear the database before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_register_user(clear_database):
    response = client.post(
        "/users/register", json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_user_existing_username(clear_database):
    client.post(
        "/users/register", json={"username": "testuser", "password": "testpassword"}
    )
    response = client.post(
        "/users/register", json={"username": "testuser", "password": "newpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_login_user(clear_database):
    client.post(
        "/users/register", json={"username": "testuser", "password": "testpassword"}
    )
    response = client.post(
        "/users/login", json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_invalid_credentials(clear_database):
    client.post(
        "/users/register", json={"username": "testuser", "password": "testpassword"}
    )
    response = client.post(
        "/users/login", json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_nonexistent_user(clear_database):
    response = client.post(
        "/users/login", json={"username": "nonexistentuser", "password": "testpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
