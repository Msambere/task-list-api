from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.db import db
from sqlalchemy import desc
from app.routes.task_routes import validate_task_id
import datetime
import requests
import os

bp = Blueprint("bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    title = validate_new_goal_data(request_body)

    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()

    response = {"goal": new_goal.to_dict()}
    return response, 201

@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    response=[goal.to_dict() for goal in goals]

    return response, 200

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal_id(goal_id)

    response = goal.to_dict()

    return {"goal":response}, 200

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal=validate_goal_id(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return {"title" : goal.title}, 200

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)
    db.session.delete(goal)
    db.session.commit()
    
    response = {
        "details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"
    }
    return response, 200

@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal=validate_goal_id(goal_id)
    request_body=request.get_json()

    task_list= request_body["task_ids"]

    for task in task_list:
        task = validate_task_id(task)
        task.goal_id = goal_id
    db.session.commit()

    task_ids =[]
    for task in goal.tasks:
        task_ids.append(task.id)
    # response= task_ids
    response = {
        "id": goal.id,
        "task_ids": task_ids
    }
    return response, 200

@bp.get("/<goal_id>/tasks")
def get_tasks_of_one_goal(goal_id):
    goal = validate_goal_id(goal_id)
    task_list = generate_tasks_list(goal)
    response = goal.to_dict()
    response["tasks"] = task_list
    return response, 200


# Helper Functions
def validate_new_goal_data(request_body):
    try:
        title = request_body["title"]
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    if not isinstance(title, str):
        response = {"msg": "Invalid book details"}
        abort(make_response(response, 400))

    return title

def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response = {"msg": f"Goal_id {goal_id} is invalid"}
        abort(make_response(response, 400))

    query = db.select(Goal).where(Goal.id == goal_id)
    found_goal = db.session.scalar(query)

    if not found_goal:
        response = {"msg": f"Goal {goal_id} not found."}
        abort(make_response(response, 404))

    return found_goal

def generate_tasks_list(goal):
        task_list=[]
        for task in goal.tasks:
            task_dict = task.to_dict()
            task_dict["goal_id"] = goal.id
            task_list.append(task_dict)
        return task_list


