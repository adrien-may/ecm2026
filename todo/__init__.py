from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import make_engine
from .models import Task
from .schemas import TaskCreate, TaskPatch, TaskRead


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

    def find_task(session, task_id):
        task = session.get(Task, task_id)
        if task is None:
            raise HTTPException(404, detail="Task not found")
        return task

    @app.get("/tasks/{task_id}", response_model=TaskRead)
    def get_task(task_id: int, session: DatabaseSession):
        return find_task(session, task_id)

    @app.patch("/tasks/{task_id}", response_model=TaskRead)
    def update_task(task_id: int, data: TaskPatch, session: DatabaseSession):
        task = find_task(session, task_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        session.commit()
        session.refresh(task)
        return task

    @app.delete("/tasks/{task_id}", status_code=204)
    def delete_task(task_id: int, session: DatabaseSession):
        session.delete(find_task(session, task_id))
        session.commit()
        return Response(status_code=204)

    return app
