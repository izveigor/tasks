import uuid
from typing import Any

from flask import Flask

from connection.pb.tasks_pb2 import IDRequest, UserRequest  # type: ignore
from connection.tasks_server import TasksService
from models import TaskUser
from tests.helpers import check_model_fields, create_user


class TestTasksServicer:
    def test_AddUser(
        self,
        testing_app: Flask,
    ) -> None:
        service = TasksService(testing_app)
        user_uuid = uuid.uuid4()
        user_data: dict[str, Any] = {
            "id": str(user_uuid),
            "username": "username",
            "image": "http://image",
        }
        request = UserRequest(**user_data)
        user_data["current_task_id"] = None
        user_data["id"] = user_uuid

        service.AddUser(request, None)

        user = TaskUser.query.all()[0]
        check_model_fields(user, user_data)

    def test_ChangeUser(
        self,
        testing_app: Flask,
    ) -> None:
        service = TasksService(testing_app)
        user_uuid = uuid.uuid4()
        user_data = {
            "id": user_uuid,
            "username": "username",
            "image": "http://image",
        }
        create_user(user_data)

        request = UserRequest(
            id=str(user_uuid),
            username="changed_username",
            image="http://changed_image",
        )
        service.ChangeUser(request, None)

        user = TaskUser.query.get(user_uuid)
        assert user.username == "changed_username"
        assert user.image == "http://changed_image"

    def test_DeleteUser(
        self,
        testing_app: Flask,
    ) -> None:
        service = TasksService(testing_app)
        user_uuid = uuid.uuid4()
        create_user(
            {
                "id": user_uuid,
                "username": "username",
                "image": "http://image",
            }
        )

        request = IDRequest(id=str(user_uuid))
        service.DeleteUser(request, None)

        assert len(TaskUser.query.all()) == 0
