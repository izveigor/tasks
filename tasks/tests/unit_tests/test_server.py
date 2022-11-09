from app.server import UsersService
from flask.testing import FlaskClient
from app.pb.users_pb2 import UserRequest, IDRequest
from models import TaskUser
from tests.helpers import create_user


class TestUsersServicer:
    def test_AddUser(
        self,
        client: FlaskClient,
    ):
        service = UsersService()
        request = UserRequest(
            id=1,
            username="username",
        )

        service.AddUser(request, None)

        users = TaskUser.query.all()
        assert len(users) == 1
        assert users[0].id == 1
        assert users[0].username == "username"

    def test_ChangeUser(
        self,
        client: FlaskClient,
    ):
        service = UsersService()
        create_user(
            {
                "id": 1,
                "username": "username",
            }
        )

        request = UserRequest(
            id=1,
            username="changed_username",
        )
        service.ChangeUser(request, None)

        user = TaskUser.query.get(1)

        assert user.username == "changed_username"

    def test_DeleteUser(
        self,
        client: FlaskClient,
    ):
        service = UsersService()
        create_user(
            {
                "id": 1,
                "username": "username",
            }
        )

        request = IDRequest(
            id=1,
        )
        service.DeleteUser(request, None)

        assert len(TaskUser.query.all()) == 0
