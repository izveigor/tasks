from app.features import get_permission, authorization_like_teammate, get_token
from flask.testing import FlaskClient
from tests.helpers import create_user, serve, check_model_fields
from unittest.mock import patch, Mock
from models import TaskUser
import uuid


class TestFeatures:

    def test_get_token(self):
        auth_header = "Token 11111"
        token = get_token(auth_header)
        assert token == "11111"

    @patch("app.features.get_token")
    def test_authorization_like_teammate(
        self,
        mock_get_token: Mock,
        client: FlaskClient,
    ):
        mock_get_token.return_value = "11111"
        print(uuid.uuid4())
        create_user({
            "id": uuid.uuid4(),
            "username": "username",
            "image": "http://image",
        })
        serve()

        request = type("", (), {"headers": {"Authorization": "11111"}})
        token, user = authorization_like_teammate(request)

        assert token == "11111"
        assert user == TaskUser.query.all()[0]

    @patch("app.features.get_token")
    def test_get_permission(
        self,
        mock_get_token: Mock,
        client: FlaskClient
    ):
        mock_get_token.return_value = "11111"
        create_user({
            "id": uuid.uuid4(),
            "username": "username",
            "image": "http://image",
        })
        serve()

        request = type("", (), {"headers": {"Authorization": "11111"}})
        token, user = get_permission(request, "username1")

        assert token == "11111"
        assert user == TaskUser.query.all()[0]
