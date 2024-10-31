
from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body['title']
    description = request_body['description']
    completed_at = request_body['completed_at']
    # title, description = validate_new_book_data(request_body)

    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = new_task.to_dict()
    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query)

    response = []
    for task in tasks:
        response.append(task.to_dict())

    return response, 200
