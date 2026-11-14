from todo import create_app
from todo.models import db


def test_new_application_reads_committed_data(tmp_path):
    config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'restart.sqlite'}",
    }
    first_app = create_app(config)
    runner = first_app.test_cli_runner()
    assert runner.invoke(args=["init-db"]).exit_code == 0
    task = first_app.test_client().post("/tasks/", json={"title": "Persistée"}).json
    with first_app.app_context():
        db.session.remove()
        db.engine.dispose()
    second_app = create_app(config)
    try:
        assert second_app.test_client().get("/tasks/").json == [task]
    finally:
        with second_app.app_context():
            db.session.remove()
            db.engine.dispose()

