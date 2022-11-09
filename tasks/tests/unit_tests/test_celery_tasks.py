from unittest.mock import patch, Mock
from app.celery_tasks import validate_task_data
from tests.helpers import create_user
from app.constants import TASK_STATUS
from models import TaskUser, Task
from datetime import datetime
from flask.testing import FlaskClient


class TestValidateTaskData:
    def create_users(self):
        receiver_user = {
            "id": 1,
            "username": "username1",
            "current_task_id": None,
        }
        sender_user = {
            "id": 2,
            "username": "username2",
            "current_task_id": None,
        }

        create_user(receiver_user)
        create_user(sender_user)

    def create_tasks(self):
        time = datetime.now()
        first_task = Task(
            id=1,
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=1,
            sender_user_id=2,
        )

        second_task = Task(
            id=2,
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=1,
            sender_user_id=2,
        )

        return first_task, second_task

    def test_validate_data_is_right(
        self,
        client: FlaskClient,
    ):
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user": TaskUser.query.filter_by(id=1).first(),
            "sender_user": TaskUser.query.filter_by(id=2).first(),
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
    ):
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user": TaskUser.query.filter_by(id=1).first(),
            "sender_user": TaskUser.query.filter_by(id=2).first(),
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
    ):
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user": TaskUser.query.filter_by(id=1).first(),
            "sender_user": TaskUser.query.filter_by(id=2).first(),
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
    ):
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user": TaskUser.query.filter_by(id=1).first(),
            "sender_user": TaskUser.query.filter_by(id=2).first(),
        }

        time = datetime.now()
        first_task = Task(
            id=1,
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=2,
            sender_user_id=1,
        )

        second_task = Task(
            id=2,
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=1,
            sender_user_id=2,
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
    ):
        self.create_users()
        task_json = {
            "status": TASK_STATUS[0],
            "receiver_user": TaskUser.query.filter_by(id=1).first(),
            "sender_user": TaskUser.query.filter_by(id=2).first(),
        }

        time = datetime.now()
        first_task = Task(
            id=1,
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=1,
            sender_user_id=2,
        )

        second_task = Task(
            id=2,
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=2,
            sender_user_id=1,
        )
        previous_tasks = [first_task]
        subsequent_tasks = [second_task]

        is_validated = validate_task_data(
            task_json,
            previous_tasks,
            subsequent_tasks,
        )

        assert not is_validated
