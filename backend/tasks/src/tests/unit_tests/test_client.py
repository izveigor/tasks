import grpc
from connte.pb.tasks_pb2 import (
    PermissionRequest,
    PermissionResponse,
    GetUserFromTokenRequest,
    GetUserFromTokenResponse,
)
from app.tasks_client import tasks_client
from concurrent import futures
from threading import Thread
from tests.helpers import serve


class TestClient:
    def test_get_user_from_token(self):
        token = "11111"
        serve()
        users_response = tasks_client.GetUserFromToken(
            GetUserFromTokenRequest(token=token)
        )

        assert users_response.username == "username"

    def test_check_permission(self):
        serve()
        users_response = tasks_client.CheckPermission(
            PermissionRequest(
                receiverUsername="username1",
                senderUsername="username2",
            )
        )

        assert users_response.is_permission_exist