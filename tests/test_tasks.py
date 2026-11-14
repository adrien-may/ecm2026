from datetime import datetime, timedelta
import pytest


def test_list_starts_empty(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json == []



def test_create_and_read(client):
    response = client.post("/tasks/", json={"title": "  Lire Flask  "})
    assert response.status_code == 201
    task = response.json
    assert type(task["id"]) is int
    assert task["title"] == "Lire Flask"
    assert task["done"] is False
    assert datetime.fromisoformat(task["creation_date"]).utcoffset() == timedelta(0)
    assert client.get("/tasks/").json == [task]



@pytest.mark.parametrize("data", [
    {}, {"title": " "}, {"title": "x" * 256}, {"title": 1},
    {"title": None}, {"title": "x", "done": True}, [], None,
])
def test_invalid_create_leaves_list_empty(client, data):
    response = client.post("/tasks/", json=data)
    assert 400 <= response.status_code < 500
    assert response.is_json
    assert client.get("/tasks/").json == []



def test_duplicate_titles_are_allowed(client):
    first = client.post("/tasks/", json={"title": "Lire"}).json
    second = client.post("/tasks/", json={"title": "Lire"}).json
    assert first["id"] != second["id"]



def test_json_and_method_errors(client):
    malformed = client.post("/tasks/", data="{", content_type="application/json")
    assert malformed.status_code == 400
    assert malformed.is_json
    wrong_type = client.post("/tasks/", data="title=Lire")
    assert wrong_type.status_code == 415
    assert wrong_type.is_json
    wrong_method = client.put("/tasks/")
    assert wrong_method.status_code == 405
    assert "GET" in wrong_method.headers["Allow"]



