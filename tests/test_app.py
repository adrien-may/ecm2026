from flask import Flask
from app import app


def test_app_is_flask():
    assert isinstance(app, Flask)
