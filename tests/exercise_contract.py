# À lancer explicitement au début de l’exercice.
def test_partial_update_and_delete_preserve_other_task(client):
    first = client.post("/tasks/", json={"title": "Lire"}).json()
    second = client.post("/tasks/", json={"title": "Tester"}).json()
    url = f"/tasks/{first['id']}"
    assert client.get(url).json() == first
    updated = client.patch(url, json={"done": True})
    assert updated.status_code == 200
    assert updated.json() == {**first, "done": True}
    renamed = client.patch(url, json={"title": " Relire "})
    assert renamed.json() == {**first, "title": "Relire", "done": True}
    response = client.delete(url)
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(url).status_code == 404
    assert client.get("/tasks/").json() == [second]

