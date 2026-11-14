from pathlib import Path

from flask import Flask, abort, render_template, request
from werkzeug.exceptions import HTTPException

from .models import Task, db


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


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///flask-todo.sqlite",
    )
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    # Configuration must be final before initializing the extension.
    db.init_app(app)

    @app.cli.command("init-db")
    def init_db():
        """Create missing tables; this does not migrate existing columns."""
        db.create_all()
        print("Database ready")

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
        query = db.select(Task).order_by(Task.id)
        tasks = db.session.scalars(query).all()
        return [task.to_dict() for task in tasks]

    @app.post("/tasks/")
    def create_task():
        task = Task(**read_fields())
        db.session.add(task)
        db.session.commit()
        return task.to_dict(), 201

    def find_task(task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            abort(404, description="Task not found")
        return task

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        return find_task(task_id).to_dict()

    @app.patch("/tasks/<int:task_id>")
    def update_task(task_id):
        task = find_task(task_id)
        fields = read_fields(partial=True)
        for key, value in fields.items():
            setattr(task, key, value)
        db.session.commit()
        return task.to_dict()

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        db.session.delete(find_task(task_id))
        db.session.commit()
        return "", 204

    return app
