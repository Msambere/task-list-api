import pytest
from app.models.task import Task
from app.models.goal import Goal
from app.routes.route_utilities import validate_new_model_data

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_validate_new_model_data():
    # Arrrange & 
    model_data = {"title": "New ADA task", "description": "Making a new model"}
    cls = Task
    # Act
    results = validate_new_model_data(cls, model_data)

    # Assert
    assert results == model_data

@pytest.mark.skip(reason="No way to test this feature yet")
def test_validate_new_model_data_missing_data():
    # Arrrange & 
    model_data = {"description": "Making a new model"}
    cls = Task
    # Act
    results = validate_new_model_data(cls, model_data)

    # Assert
    assert results == model_data
