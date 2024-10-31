
from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body['title']
    description = request_body['description']

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    response = {"task":new_task.to_dict()}
    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query)

    response = []
    for task in tasks:
        response.append(task.to_dict())

    return response, 200

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task_id(task_id)
    return {
        "task":task.to_dict()
    }, 200



# Helper Function
def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"msg":f"Task id {task_id} is invalid"}
        abort(make_response(response, 400))

    query = db.select(Task).where(Task.id == task_id)
    found_task = db.session.scalar(query)

    if not found_task:
        response = {"msg":f"Task {task_id} not found."}
        abort(make_response(response, 404))

    return found_task
    
