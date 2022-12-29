import uuid
from unittest.mock import Mock, patch

from flask.testing import FlaskClient

from app.features import authorization_like_teammate, get_permission, get_token
from models import TaskUser
from tests.helpers import check_model_fields, create_user, serve


class TestFeatures:
    def test_get_token(self) -> None:
        auth_header = "Token 11111"
        token = get_token(auth_header)
        assert token == "11111"

    @patch("app.features.get_token")
    def test_authorization_like_teammate(
        self,
        mock_get_token: Mock,
        client: FlaskClient,
    ) -> None:
        mock_get_token.return_value = "11111"
        create_user(
            {
                "id": uuid.uuid4(),
                "username": "username",
                "image": "http://image",
            }
        )
        serve()

        request = type("", (), {"headers": {"Authorization": "11111"}})
        token, user = authorization_like_teammate(request)

        assert token == "11111"
        assert user == TaskUser.query.all()[0]

    @patch("app.features.get_token")
    def test_get_permission(self, mock_get_token: Mock, client: FlaskClient) -> None:
        mock_get_token.return_value = "11111"
        create_user(
            {
                "id": uuid.uuid4(),
                "username": "username",
                "image": "http://image",
            }
        )
        serve()

        request = type("", (), {"headers": {"Authorization": "11111"}})
        token, user = get_permission(request, "username1")

        assert token == "11111"
        assert user == TaskUser.query.all()[0]
