from flask import abort, request
from flask_smorest import Blueprint

from .models import Task, db
from .schemas import TaskPatchSchema, TaskSchema


tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_blueprint.get("/")
@tasks_blueprint.response(200, TaskSchema(many=True))
def list_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query).all()
    return tasks

@tasks_blueprint.post("/")
@tasks_blueprint.arguments(TaskSchema, error_status_code=400)
@tasks_blueprint.response(201, TaskSchema)
def create_task(data):
    task = Task(**data)
    db.session.add(task)
    db.session.commit()
    return task

def find_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404, description="Task not found")
    return task

@tasks_blueprint.before_request
def check_write_request():
    if request.method == "PATCH":
        find_task(request.view_args["task_id"])
    if request.method in {"POST", "PATCH"}:
        request.get_json()


@tasks_blueprint.get("/<int:task_id>")
@tasks_blueprint.response(200, TaskSchema)
def get_task(task_id):
    return find_task(task_id)

@tasks_blueprint.patch("/<int:task_id>")
@tasks_blueprint.arguments(
    TaskPatchSchema(partial=True), error_status_code=400
)
@tasks_blueprint.response(200, TaskSchema)
def update_task(fields, task_id):
    task = find_task(task_id)
    for key, value in fields.items():
        setattr(task, key, value)
    db.session.commit()
    return task

@tasks_blueprint.delete("/<int:task_id>")
@tasks_blueprint.response(204)
def delete_task(task_id):
    db.session.delete(find_task(task_id))
    db.session.commit()
    return None

