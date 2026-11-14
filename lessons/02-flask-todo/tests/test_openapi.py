def test_openapi_describes_tasks(client):
    response = client.get("/openapi/openapi.json")
    assert response.status_code == 200
    spec = response.get_json()
    post = spec["paths"]["/tasks/"]["post"]
    assert post["requestBody"]["required"] is True
    assert "201" in post["responses"]
    task = spec["components"]["schemas"]["Task"]
    assert task["required"] == ["title"]


def test_swagger_ui_is_available(client):
    response = client.get("/openapi/swagger")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "SwaggerUIBundle" in html
    assert "/openapi/openapi.json" in html
