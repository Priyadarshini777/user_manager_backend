from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Welcome to User Manager API!"}


def test_create_and_get_user():
    res = client.post("/users", json={"id": 1, "name": "Priya"})
    assert res.status_code == 200
    data = res.json()
    assert data["user"]["name"] == "Priya"

    res_get = client.get("/users/1")
    assert res_get.status_code == 200
    assert res_get.json()["name"] == "Priya"
