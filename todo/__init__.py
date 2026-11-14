from datetime import datetime, timezone

from flask import Flask, abort, render_template, request
from werkzeug.exceptions import HTTPException


def read_fields(*, partial=False):
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description="Expected a JSON object")
    allowed = {"title", "done"} if partial else {"title"}
    if not data or set(data) - allowed:
        abort(400, description="Unexpected or missing fields")
    if not partial and "title" not in data:
        abort(400, description="title is required")
    if "title" in data:
        if not isinstance(data["title"], str):
            abort(400, description="title must be a string")
        data["title"] = data["title"].strip()
        if not 1 <= len(data["title"]) <= 255:
            abort(400, description="title must contain 1 to 255 characters")
    if "done" in data and type(data["done"]) is not bool:
        abort(400, description="done must be a boolean")
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

    def find_task(task_id):
        if task_id not in tasks:
            abort(404, description="Task not found")
        return tasks[task_id]

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        return find_task(task_id)

    @app.patch("/tasks/<int:task_id>")
    def update_task(task_id):
        task = find_task(task_id)
        task.update(read_fields(partial=True))
        return task

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        find_task(task_id)
        del tasks[task_id]
        return "", 204

    return app
