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
    test_user = User(
        username="testuser",
        hashed_password=hashed_password,
        balance=100,
        message_count=0,
    )
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
def test_send_message_without_winning():
    token = authenticate_user()
    response = client.post(
        "/messages/send",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] in [
        "Sorry, better luck next time!",
        "Congratulations! You won the pot!",
    ]
    assert "pot_amount" in response.json()

    # Check balance and pot update
    balance_response = client.get(
        "/currency/balance", headers={"Authorization": f"Bearer {token}"}
    )
    assert balance_response.status_code == 200
    balance = balance_response.json()["balance"]
    assert balance == 95  # Message cost = 5 for first message

    pot_response = client.get("/pot/")
    assert pot_response.status_code == 200
    pot_amount = pot_response.json()["pot_amount"]
    assert pot_amount == 5  # Pot should increase by message cost


def test_send_message_with_winning_logic():
    token = authenticate_user()

    # Start the test with a high balance
    initial_balance_response = client.get(
        "/currency/balance", headers={"Authorization": f"Bearer {token}"}
    )
    assert initial_balance_response.status_code == 200
    initial_balance = initial_balance_response.json()["balance"]

    if initial_balance < 500:  # Ensure at least 500 units are available
        client.post(
            "/currency/deduct",
            params={"cost": -500 + initial_balance},
            headers={"Authorization": f"Bearer {token}"},
        )

    # Simulate multiple messages to ensure a chance of winning
    for _ in range(20):
        response = client.post(
            "/messages/send",
            headers={"Authorization": f"Bearer {token}"},
        )
        if (
            response.status_code == 200
            and response.json()["message"] == "Congratulations! You won the pot!"
        ):
            break
        elif (
            response.status_code == 400
            and response.json()["detail"] == "Insufficient balance"
        ):
            pytest.fail("Insufficient balance before winning occurred")
    else:
        pytest.fail("No winning message received after 20 attempts")

    # Ensure pot reset
    pot_response = client.get("/pot/")
    assert pot_response.status_code == 200
    assert pot_response.json()["pot_amount"] == 0


def test_insufficient_balance_for_message():
    token = authenticate_user()

    # Deduct balance until insufficient
    while True:
        response = client.post(
            "/messages/send",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code == 400:  # Insufficient balance error
            assert response.json()["detail"] == "Insufficient balance"
            break

    # Verify balance is less than the next message cost
    balance_response = client.get(
        "/currency/balance", headers={"Authorization": f"Bearer {token}"}
    )
    assert balance_response.status_code == 200
    balance = balance_response.json()["balance"]

    # Fetch user details to calculate the next message cost
    user_response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert user_response.status_code == 200
    message_count = user_response.json()["message_count"]

    next_message_cost = 5 * (message_count + 1)  # Dynamic pricing formula

    assert (
        balance < next_message_cost
    )  # Balance must be insufficient for the next message
