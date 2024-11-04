from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.db import db
from sqlalchemy import desc
import datetime
import requests
import os
from app.routes.route_utilities import validate_model_id

bp = Blueprint("bp", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    request_body = request.get_json()
    title, description = validate_new_task_data(request_body)

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    response = {"task": new_task.to_dict()}
    return response, 201


@bp.get("")
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


@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model_id(Task, task_id)
    task_dict=task.to_dict()
    if task.goal_id:
        task_dict["goal_id"]= task.goal_id
    return {"task": task_dict}, 200


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model_id(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return {"task": task.to_dict()}, 200


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model_id(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    response = {"details": f'Task {task_id} "{task.title}" successfully deleted'}
    return response, 200


@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model_id(Task, task_id)

    task.completed_at = datetime.datetime.now()
    db.session.commit()

    notification = send_task_completion_slack(task)

    if notification:
        return {"task": task.to_dict()}, 200


@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model_id(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return {"task": task.to_dict()}, 200


# Helper Function

def validate_new_task_data(request_body):
    try:
        title = request_body["title"]
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    try:
        description = request_body["description"]
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    if not isinstance(title, str) or not isinstance(description, str):
        response = {"msg": "Invalid book details"}
        abort(make_response(response, 400))

    return title, description

def send_task_completion_slack(task):
    url = "https://slack.com/api/chat.postMessage"
    api_key = os.environ.get("SLACK_BOT_TOKEN")
    header = {"Authorization": f"Bearer {api_key}"}
    request_body = {
        "channel": "C07UJK253A7",
        "text": f"Someone just completed the task {task.title}",
    }

    return requests.post(url, headers=header, params=request_body)