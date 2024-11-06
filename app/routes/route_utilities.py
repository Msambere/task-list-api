from flask import abort, make_response
import inspect
from ..db import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc

def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"msg": f"{cls.__name__} id {model_id} is invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    found_model = db.session.scalar(query)

    if not found_model:
        response = {"msg": f"{cls.__name__} {model_id} not found."}
        abort(make_response(response, 404))

    return found_model

def create_model(cls, model_data):
    valid_model_data = validate_new_model_data(cls, model_data)

    new_model = cls.from_dict(valid_model_data)
    db.session.add(new_model)
    db.session.commit()

    response = {cls.__name__.lower(): new_model.to_dict()}
    return response, 201

def get_models_with_filters(cls, filter_params=None):
    query = db.select(cls)
    if filter_params:
        for param, value in filter_params.items():
            if param != "order_by" and param != "sort" and  hasattr(cls, param):
                query = query.where(getattr(cls, param).ilike(f"%{value}%"))
        
        if "order_by" in filter_params:
            order_by = getattr(cls,filter_params["order_by"])
        else:
            order_by = cls.title

        if "sort" in filter_params:
            if filter_params["sort"] == "desc":
                query = query.order_by(desc(order_by))
            else:
                query = query.order_by(order_by)
                

    models = db.session.scalars(query)

    response = [model.to_dict() for model in models]
    return response, 200
    

def delete_record(cls, model_id):
    model = validate_model_id(cls, model_id)
    db.session.delete(model)
    db.session.commit()
    
    response = {
        "details": f"{cls.__name__} {model.id} \"{model.title}\" successfully deleted"
    }
    return response, 200

#helper function
def validate_new_model_data(cls, model_data):
# import inspect
# class_attributes = inspect.getargspec(Thing).args)
# class_attributes.pop("id")

    class_attributes = []
    if cls == Goal or cls == Task:
        class_attributes.append("title")
    if cls == Task:
        class_attributes.append("description")

    for attribute in class_attributes:
        try:
            attribute = model_data[attribute]
        except:
            response = {"details": "Invalid data"}
            abort(make_response(response, 400))

    return model_data