from flask import Flask
from app import app


def test_app_is_flask():
    assert isinstance(app, Flask)


def test_default_page():
    client = app.test_client()
    response = client.get("/bonjour")
    assert response.status_code == 200
    assert "Bonjour ECM" in response.get_data(as_text=True)


def test_page_displays_samira():
    client = app.test_client()
    response = client.get("/bonjour?name=Samira")
    assert "Bonjour Samira" in response.get_data(as_text=True)


def test_page_displays_elodie():
    client = app.test_client()
    response = client.get("/bonjour?name=Élodie")
    assert "Bonjour Élodie" in response.get_data(as_text=True)


def test_page_escapes_name():
    client = app.test_client()
    name = "<script>alert(1)</script>"
    response = client.get("/bonjour", query_string={"name": name})
    html = response.get_data(as_text=True)
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert name not in html
