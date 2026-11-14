from datetime import datetime, timezone

from flask import Flask, abort, render_template, request
from werkzeug.exceptions import HTTPException


def read_fields():
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description="Expected a JSON object")
    if set(data) != {"title"}:
        abort(400, description="Expected only title")
    if not isinstance(data["title"], str):
        abort(400, description="title must be a string")
    data["title"] = data["title"].strip()
    if not 1 <= len(data["title"]) <= 255:
        abort(400, description="title must contain 1 to 255 characters")
    return data


def create_app():
    app = Flask(__name__)
    tasks = {}
    next_id = 1

    @app.errorhandler(HTTPException)
    def http_error(error):
        # Retain protocol headers, e.g. Allow on a 405 response.
        response = error.get_response()
        response.data = app.json.dumps({"error": error.description})
        response.content_type = "application/json"
        return response

    @app.get("/bonjour")
    def hello():
        name = request.args.get("name", "ECM")
        return render_template("hello.html", name=name)

    @app.get("/api/bonjour")
    def hello_json():
        name = request.args.get("name", "ECM")
        return {"message": f"Bonjour {name}"}

    @app.get("/tasks/")
    def list_tasks():
        return list(tasks.values())

    @app.post("/tasks/")
    def create_task():
        nonlocal next_id
        data = read_fields()
        task = {
            "id": next_id, "title": data["title"], "done": False,
            "creation_date": datetime.now(timezone.utc).isoformat(),
        }
        tasks[next_id] = task
        next_id += 1
        return task, 201

    return app
