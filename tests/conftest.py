import pytest
from fastapi.testclient import TestClient

from todo import create_app
from sqlmodel import SQLModel


@pytest.fixture
def app(tmp_path):
    app = create_app(f"sqlite:///{tmp_path / 'test.sqlite'}")
    SQLModel.metadata.create_all(app.state.engine)
    yield app
    app.state.engine.dispose()


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client
