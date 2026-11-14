from datetime import datetime, timedelta
import pytest


def test_list_starts_empty(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json == []



