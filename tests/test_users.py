from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/users/", json={"name": "test_user"})
    assert response.status_code == 200
    assert response.json()["name"] == "test_user"
