import pytest
from fastapi.testclient import TestClient

from scores import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(f"sqlite:///{tmp_path / 'test.sqlite'}")
    with TestClient(app) as client:
        yield client
    app.state.engine.dispose()


def test_save_normalizes_name_and_returns_generated_fields(client):
    result = client.post("/scores/", json={"player": " Samira ", "points": 60})
    assert result.status_code == 201
    score = result.json()
    assert score["player"] == "Samira"
    assert score["points"] == 60
    assert type(score["id"]) is int
    assert "+00:00" in score["created_at"]
    assert client.get("/scores/").json() == [score]


@pytest.mark.parametrize("data", [
    {"player": " ", "points": 1}, {"player": "x" * 25, "points": 1},
    {"player": "A", "points": -1}, {"player": "A", "points": 91},
    {"player": "A", "points": True}, {"player": "A", "points": "60"},
    {"player": "A", "points": 1.5}, {"player": "A", "points": 1, "id": 8},
])
def test_invalid_score_is_not_saved(client, data):
    assert client.post("/scores/", json=data).status_code == 422
    assert client.get("/scores/").json() == []


def test_leaderboard_is_sorted_limited_and_stable_for_ties(client):
    first = client.post("/scores/", json={"player": "First", "points": 50}).json()
    second = client.post("/scores/", json={"player": "Second", "points": 50}).json()
    for points in range(12):
        client.post("/scores/", json={"player": "Other", "points": points})
    rows = client.get("/scores/").json()
    assert len(rows) == 10
    assert rows[:2] == [first, second]
    assert [r["points"] for r in rows] == [50, 50, 11, 10, 9, 8, 7, 6, 5, 4]


def test_data_survives_new_application(tmp_path):
    url = f"sqlite:///{tmp_path / 'restart.sqlite'}"
    app = create_app(url)
    with TestClient(app) as client:
        client.post("/scores/", json={"player": "A", "points": 30})
    app.state.engine.dispose()
    other = create_app(url)
    try:
        with TestClient(other) as client:
            assert client.get("/scores/").json()[0]["points"] == 30
    finally:
        other.state.engine.dispose()
