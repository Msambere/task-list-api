from flask import abort, make_response
from ..db import db

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

def delete_record(cls, model_id):
    model = validate_model_id(cls, model_id)
    db.session.delete(model)
    db.session.commit()
    
    response = {
        "details": f"{cls.__name__} {model.id} \"{model.title}\" successfully deleted"
    }
    return response, 200