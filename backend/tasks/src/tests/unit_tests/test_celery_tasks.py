import uuid
from datetime import datetime
from unittest.mock import Mock, patch

from flask.testing import FlaskClient

from app.celery_tasks import validate_task_data
from constants import TASK_STATUS
from models import Task, TaskUser
from tests.helpers import create_user


class TestValidateTaskData:
    uuids = [uuid.uuid4() for _ in range(2)]

    def create_users(self) -> None:
        receiver_user = {
            "id": self.uuids[0],
            "username": "username1",
            "image": "http://image1",
            "current_task_id": None,
        }
        sender_user = {
            "id": self.uuids[1],
            "username": "username2",
            "image": "http://image2",
            "current_task_id": None,
        }

        create_user(receiver_user)
        create_user(sender_user)

    def create_tasks(self) -> tuple[Task, Task]:
        time = datetime.now()
        first_task = Task(
            id=1,
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=self.uuids[0],
            sender_user_id=self.uuids[1],
        )

        second_task = Task(
            id=2,
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=self.uuids[0],
            sender_user_id=self.uuids[1],
        )

        return first_task, second_task

    def test_validate_data_is_right(
        self,
        client: FlaskClient,
    ) -> None:
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user_id": self.uuids[0],
            "sender_user_id": self.uuids[1],
        }

        first_task, second_task = self.create_tasks()
        previous_tasks = [first_task]
        subsequent_tasks = [second_task]

        is_validated = validate_task_data(
            task_json,
            previous_tasks,
            subsequent_tasks,
        )

        assert is_validated

    def test_circular_problem_with_previous_tasks(
        self,
        client: FlaskClient,
    ) -> None:
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user_id": self.uuids[0],
            "sender_user_id": self.uuids[1],
        }

        first_task, second_task = self.create_tasks()
        previous_tasks = [first_task, second_task]
        subsequent_tasks = [second_task]

        is_validated = validate_task_data(
            task_json,
            previous_tasks,
            subsequent_tasks,
        )

        assert not is_validated

    def test_circular_problem_with_subsequent_tasks(
        self,
        client: FlaskClient,
    ) -> None:
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user_id": self.uuids[0],
            "sender_user_id": self.uuids[1],
        }

        first_task, second_task = self.create_tasks()
        previous_tasks = [first_task]
        subsequent_tasks = [first_task, second_task]

        is_validated = validate_task_data(
            task_json,
            previous_tasks,
            subsequent_tasks,
        )

        assert not is_validated

    def test_equality_with_previous_tasks(
        self,
        client: FlaskClient,
    ) -> None:
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user_id": self.uuids[0],
            "sender_user_id": self.uuids[1],
        }

        time = datetime.now()
        first_task = Task(
            id=1,
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=self.uuids[1],
            sender_user_id=self.uuids[0],
        )

        second_task = Task(
            id=2,
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=self.uuids[0],
            sender_user_id=self.uuids[1],
        )
        previous_tasks = [first_task]
        subsequent_tasks = [second_task]

        is_validated = validate_task_data(
            task_json,
            previous_tasks,
            subsequent_tasks,
        )

        assert not is_validated

    def test_equality_with_subsequent_tasks(
        self,
        client: FlaskClient,
    ) -> None:
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user_id": self.uuids[0],
            "sender_user_id": self.uuids[1],
        }

        time = datetime.now()
        first_task = Task(
            id=1,
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=self.uuids[0],
            sender_user_id=self.uuids[1],
        )

        second_task = Task(
            id=2,
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=self.uuids[1],
            sender_user_id=self.uuids[0],
        )
        previous_tasks = [first_task]
        subsequent_tasks = [second_task]

        is_validated = validate_task_data(
            task_json,
            previous_tasks,
            subsequent_tasks,
        )

        assert not is_validated
