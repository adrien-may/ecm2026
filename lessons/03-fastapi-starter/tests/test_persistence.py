from fastapi.testclient import TestClient

from todo import create_app
from todo.models import Base


def test_new_application_reads_committed_data(tmp_path):
    url = f"sqlite:///{tmp_path / 'restart.sqlite'}"
    first = create_app(url)
    Base.metadata.create_all(first.state.engine)
    with TestClient(first) as client:
        task = client.post("/tasks/", json={"title": "Persistée"}).json()
    first.state.engine.dispose()
    second = create_app(url)
    try:
        with TestClient(second) as client:
            assert client.get("/tasks/").json() == [task]
    finally:
        second.state.engine.dispose()


def test_cors_allows_only_classroom_client(client):
    response = client.options("/tasks/", headers={
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "PATCH",
        "Access-Control-Request-Headers": "content-type",
    })
    assert response.headers["Access-Control-Allow-Origin"] == "http://localhost:5173"
    response = client.get("/tasks/", headers={"Origin": "https://unrelated.example"})
    assert "Access-Control-Allow-Origin" not in response.headers
