from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.db import db
from sqlalchemy import desc
import datetime
import requests
import os

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    title = validate_new_goal_data(request_body)

    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()

    response = {"goal": new_goal.to_dict()}
    return response, 201


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