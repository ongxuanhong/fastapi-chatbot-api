import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.db.database import Base, get_db
from app.core.auth import hash_password
from app.db.models import User

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
def test_get_balance():
    token = authenticate_user()
    response = client.get(
        "/currency/balance", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 100


def test_deduct_balance():
    token = authenticate_user()
    response = client.post(
        "/currency/deduct",
        params={"cost": 10},  # Pass cost as a query parameter
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["new_balance"] == 90


def test_deduct_insufficient_balance():
    token = authenticate_user()
    response = client.post(
        "/currency/deduct",
        params={"cost": 200},  # Pass cost as a query parameter
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"


def test_get_balance_after_deduction():
    token = authenticate_user()
    response = client.get(
        "/currency/balance", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 90
