from flask import Flask
from app import app


def test_app_is_flask():
    assert isinstance(app, Flask)


def test_default_page():
    client = app.test_client()
    response = client.get("/bonjour")
    assert response.status_code == 200
    assert "Bonjour ECM" in response.get_data(as_text=True)
