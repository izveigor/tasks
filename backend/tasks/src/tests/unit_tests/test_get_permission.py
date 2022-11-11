from app.get_permission import get_permission
from tests.helpers import serve
from flask.testing import FlaskClient


def test_get_user(client: FlaskClient):
    serve()
    is_permission_exist = get_permission("username1", "username2")
    assert is_permission_exist
