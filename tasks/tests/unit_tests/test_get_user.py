from app.get_user import get_user
from tests.helpers import create_user, serve, check_model_fields
from flask.testing import FlaskClient


def test_get_user(client: FlaskClient):
    user_data = {
        "id": 1,
        "username": "username",
        "current_task_id": None,
    }
    create_user(user_data)
    serve()
    user_model = get_user(token="11111")
    check_model_fields(user_model, user_data)
