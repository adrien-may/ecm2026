import pytest
from flask import Flask


def test_app_is_flask(app):
    assert isinstance(app, Flask)


def test_default_page(client):
    response = client.get("/bonjour")
    assert response.status_code == 200
    assert "Bonjour ECM" in response.get_data(as_text=True)


@pytest.mark.parametrize("name", ["Samira", "Élodie"])
def test_page_displays_requested_name(client, name):
    response = client.get(
        "/bonjour", query_string={"name": name}
    )
    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert f"Bonjour {name}" in response.get_data(as_text=True)


def test_page_escapes_name(client):
    name = "<script>alert(1)</script>"
    response = client.get("/bonjour", query_string={"name": name})
    html = response.get_data(as_text=True)
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert name not in html


def test_page_matches_its_template(app, client):
    # Comparaison pédagogique : le résultat attendu utilise le même template.
    response = client.get(
        "/bonjour", query_string={"name": "Samira"}
    )
    template = app.jinja_env.get_template("hello.html")
    expected = template.render(name="Samira")
    assert response.get_data(as_text=True) == expected


def test_api_returns_json(client):
    response = client.get("/api/bonjour?name=Samira")
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.json == {"message": "Bonjour Samira"}
