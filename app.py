from flask import Flask, render_template, request

app = Flask(__name__)


@app.get("/bonjour")
def hello():
    name = request.args.get("name", "ECM")
    return render_template("hello.html", name=name)
