from fastapi.testclient import TestClient
from scores import create_app


def test_leaderboard_starts_empty(tmp_path):
    app = create_app(f"sqlite:///{tmp_path / 'test.sqlite'}")
    try:
        with TestClient(app) as client:
            response = client.get("/scores/")
            assert response.status_code == 200
            assert response.json() == []
    finally:
        app.state.engine.dispose()
