from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import make_engine
from .models import Task
from .schemas import TaskCreate, TaskRead


def create_app(database_url=None):
    app = FastAPI(title="ECM · Todo API")
    engine = make_engine(database_url)
    app.state.engine = engine
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Content-Type"],
    )

    def get_session():
        with Session(engine) as session:
            yield session

    DatabaseSession = Annotated[Session, Depends(get_session)]

    @app.get("/tasks/", response_model=list[TaskRead])
    def list_tasks(session: DatabaseSession):
        return session.scalars(select(Task).order_by(Task.id)).all()

    @app.post("/tasks/", response_model=TaskRead, status_code=201)
    def create_task(data: TaskCreate, session: DatabaseSession):
        task = Task(**data.model_dump())
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    return app
