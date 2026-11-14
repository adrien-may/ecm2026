from pathlib import Path

from flask import Flask, render_template, request
from flask_cors import CORS
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from .models import db
from .tasks import tasks_blueprint


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///flask-todo.sqlite",
        CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"],
    )
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    # Configuration must be final before initializing the extension.
    db.init_app(app)
    CORS(app, resources={r"/tasks/*": {"origins": app.config["CORS_ORIGINS"]}})

    @app.cli.command("init-db")
    def init_db():
        """Create missing tables; this does not migrate existing columns."""
        db.create_all()
        print("Database ready")

    @app.errorhandler(ValidationError)
    def validation_error(error):
        body = {"error": "Invalid task fields"}
        body["details"] = error.messages
        return body, 400

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

    app.register_blueprint(tasks_blueprint)
    return app
