
from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.db import db
from sqlalchemy import desc

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    title, description = validate_new_task_data(request_body)

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    response = {"task":new_task.to_dict()}
    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")
    query = db.select(Task)
    if sort_param == "asc":
        query = query.order_by(Task.title)
    if sort_param == "desc":
        query = query.order_by(desc(Task.title))

    tasks = db.session.scalars(query)

    
    response = [task.to_dict() for task in tasks]

    return response, 200

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task_id(task_id)
    return {
        "task":task.to_dict()
        }, 200

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()

    task.title = request_body['title']
    task.description = request_body['description']
    db.session.commit()

    return {
        "task":task.to_dict()
        }, 200
    
@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()
    response = {
        "details":f"Task {task_id} \"{task.title}\" successfully deleted"
    }
    return response, 200


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
    
def validate_new_task_data(request_body):
    try:
        title = request_body['title']
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    try:
        description = request_body['description']
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    if not isinstance(title, str) or not isinstance(description, str):
        response = {"msg": "Invalid book details"}
        abort(make_response(response, 400))

    return title, description