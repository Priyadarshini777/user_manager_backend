from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test GET /"""
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Welcome to User Manager API!"}


def test_create_user_success():
    """Test POST /users with valid data"""
    user_data = {"id": 1, "name": "Priya"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 200
    data = res.json()
    assert data["user"]["name"] == "Priya"
    assert data["user"]["id"] == 1


def test_get_user_success():
    """Test GET /users/{id} for existing user"""
    res_get = client.get("/users/1")
    assert res_get.status_code == 200
    data = res_get.json()
    assert data["name"] == "Priya"
    assert data["id"] == 1


def test_get_user_not_found():
    """Test GET /users/{id} for non-existing user"""
    res_get = client.get("/users/999")
    assert res_get.status_code == 404


def test_create_user_missing_field():
    """Test POST /users with missing field"""
    user_data = {"id": 2}  # missing 'name'
    res = client.post("/users", json=user_data)
    assert res.status_code == 422  # validation error


def test_create_user_invalid_type():
    """Test POST /users with invalid type"""
    user_data = {"id": "abc", "name": "Bob"}  # id must be int
    res = client.post("/users", json=user_data)
    assert res.status_code == 422
