from flask import Flask, render_template

app = Flask(__name__)


@app.get("/bonjour")
def hello():
    return render_template("hello.html")
