import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.db.database import Base, get_db
from app.core.auth import hash_password
from app.db.models import User, Pot

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)


# Setup test database
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Create a test user
    hashed_password = hash_password("testpassword")
    test_user = User(username="testuser", hashed_password=hashed_password, balance=100)
    db.add(test_user)

    # Create initial pot
    initial_pot = Pot(amount=0)
    db.add(initial_pot)

    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


# Helper function to get token
def authenticate_user():
    response = client.post(
        "/users/login", json={"username": "testuser", "password": "testpassword"}
    )
    return response.json()["access_token"]


# Tests
def test_get_initial_pot():
    response = client.get("/pot/")
    assert response.status_code == 200
    assert response.json()["pot_amount"] == 0


def test_contribute_to_pot():
    token = authenticate_user()
    response = client.post(
        "/pot/contribute",
        params={"contribution": 50},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["new_pot_amount"] == 50


def test_get_updated_pot():
    response = client.get("/pot/")
    assert response.status_code == 200
    assert response.json()["pot_amount"] == 50


def test_reset_pot():
    token = authenticate_user()
    response = client.post(
        "/pot/reset",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["new_pot_amount"] == 0
