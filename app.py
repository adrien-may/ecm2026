from flask import Flask

app = Flask(__name__)


@app.get("/bonjour")
def hello():
    return "<h1>Bonjour ECM</h1>"
