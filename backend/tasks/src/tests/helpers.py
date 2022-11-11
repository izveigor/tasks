from models import db, TaskUser
from typing import Any
import grpc
from app.pb import tasks_pb2_grpc
from app.pb.tasks_pb2 import (
    PermissionRequest,
    PermissionResponse,
    GetUserFromTokenRequest,
    GetUserFromTokenResponse,
)
from concurrent import futures
from threading import Thread
from app.constants import TASKS_HOST


class TasksServicer(tasks_pb2_grpc.TasksServicer):
    def CheckPermission(self, request, context):
        return PermissionResponse(
            is_permission_exist=True,
        )

    def GetUserFromToken(self, request, context):
        return GetUserFromTokenResponse(
            username="username",
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    tasks_pb2_grpc.add_TasksServicer_to_server(TasksServicer(), server)
    server.add_insecure_port(TASKS_HOST)
    server.start()


def create_user(userData: dict[str, Any]):
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
