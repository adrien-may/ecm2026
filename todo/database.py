from pathlib import Path

from sqlalchemy import create_engine


def make_engine(database_url=None):
    if database_url is None:
        folder = Path(__file__).resolve().parent.parent / "instance"
        folder.mkdir(exist_ok=True)
        database_url = f"sqlite:///{folder / 'fastapi-todo.sqlite'}"
    return create_engine(database_url, connect_args={"check_same_thread": False})
