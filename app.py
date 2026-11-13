from flask import Flask, render_template, request


def create_app():
    app = Flask(__name__)

    @app.get("/bonjour")
    def hello():
        name = request.args.get("name", "ECM")
        return render_template("hello.html", name=name)

    return app
