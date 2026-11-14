from flask import Blueprint, abort, request

from .models import Task, db
from .schemas import TaskPatchSchema, TaskSchema


tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_blueprint.get("/")
def list_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query).all()
    return TaskSchema(many=True).dump(tasks)

@tasks_blueprint.post("/")
def create_task():
    data = TaskSchema().load(request.get_json())
    task = Task(**data)
    db.session.add(task)
    db.session.commit()
    return TaskSchema().dump(task), 201

def find_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404, description="Task not found")
    return task

@tasks_blueprint.get("/<int:task_id>")
def get_task(task_id):
    return TaskSchema().dump(find_task(task_id))

@tasks_blueprint.patch("/<int:task_id>")
def update_task(task_id):
    task = find_task(task_id)
    schema = TaskPatchSchema(partial=True)
    fields = schema.load(request.get_json())
    for key, value in fields.items():
        setattr(task, key, value)
    db.session.commit()
    return TaskSchema().dump(task)

@tasks_blueprint.delete("/<int:task_id>")
def delete_task(task_id):
    db.session.delete(find_task(task_id))
    db.session.commit()
    return "", 204

