import uuid
from concurrent import futures
from typing import Any

import grpc

from connection.pb import users_pb2_grpc
from connection.pb.users_pb2 import (  # type: ignore
    AuthorizationRequest,
    AuthorizationResponse,
    PermissionRequest,
)
from constants import USERS_HOST
from models import TaskUser, db


class UsersServicer(users_pb2_grpc.UsersServicer):
    def AuthorizationLikeTeammate(
        self, request: AuthorizationRequest, context: Any
    ) -> AuthorizationResponse:
        if request.token == "11111":
            return AuthorizationResponse(is_permission_exist=True, username="username")
        return AuthorizationResponse(
            is_permission_exist=False,
            username="",
        )

    def CheckPermission(
        self, request: PermissionRequest, context: Any
    ) -> AuthorizationResponse:
        if request.senderToken == "11111" and request.receiverUsername == "username1":
            return AuthorizationResponse(is_permission_exist=True, username="username")
        return AuthorizationResponse(
            is_permission_exist=False,
            username="",
        )


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    users_pb2_grpc.add_UsersServicer_to_server(UsersServicer(), server)
    server.add_insecure_port(USERS_HOST)
    server.start()


def create_user(userData: dict[str, Any]) -> None:
    user = TaskUser(**userData)

    db.session.add(user)
    db.session.commit()


def check_model_fields(model: db.Model, data: dict[Any, Any], *args) -> None:
    fields: dict[str, Any] = vars(model)
    fields.pop("_sa_instance_state")

    for delete_field in args:
        fields.pop(delete_field)

    for key in fields.keys():
        assert fields[key] == data[key]


def create_receiver_and_sender_users() -> tuple[dict[str, Any], dict[str, Any]]:
    receiver_user: dict[str, Any] = {
        "id": uuid.uuid4(),
        "username": "username1",
        "image": "http://image1",
        "current_task_id": None,
    }
    sender_user: dict[str, Any] = {
        "id": uuid.uuid4(),
        "username": "username2",
        "image": "http://image2",
        "current_task_id": None,
    }

    create_user(receiver_user)
    create_user(sender_user)

    return receiver_user, sender_user
