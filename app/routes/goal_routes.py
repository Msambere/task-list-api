from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.db import db
from sqlalchemy import desc
import datetime
import requests
import os

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


