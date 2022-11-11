from tabnanny import check
from flask.testing import FlaskClient

from models import TaskUser, db, Task
from tests.helpers import check_model_fields, create_user
from app.constants import TASK_STATUS
from datetime import datetime, timezone


class TestModels:
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

    simple_user = {
        "id": 3,
        "username": "username3",
        "current_task_id": None,
    }

    def test_user(self, client: FlaskClient) -> None:
        create_user(self.simple_user)
        check_model_fields(TaskUser.query.all()[0], self.simple_user)

    def test_task(self, client: FlaskClient) -> None:
        first_previous_task = {
            "id": 1,
            "title": "Выполнить задание 1",
            "time": datetime.now(),
            "description": "Описание отсутствует.",
            "status": TASK_STATUS[0],
            "receiver_user_id": 1,
            "sender_user_id": 2,
        }

        second_previous_task = {
            "id": 2,
            "title": "Выполнить задание 3",
            "time": datetime.now(),
            "description": "Описание отсутствует.",
            "status": TASK_STATUS[0],
            "receiver_user_id": 1,
            "sender_user_id": 2,
        }

        first_subsequent_task = {
            "id": 3,
            "title": "Выполнить задание 2",
            "time": datetime.now(),
            "description": "Описание отсутствует.",
            "status": TASK_STATUS[0],
            "receiver_user_id": 1,
            "sender_user_id": 2,
        }

        second_subsequent_task = {
            "id": 4,
            "title": "Выполнить задание 4",
            "time": datetime.now(),
            "description": "Описание отсутствует.",
            "status": TASK_STATUS[0],
            "receiver_user_id": 1,
            "sender_user_id": 2,
        }

        task_data = {
            "id": 5,
            "title": "Выполнить задание 3",
            "time": datetime.now(),
            "description": "Описание отсутствует.",
            "status": TASK_STATUS[0],
            "receiver_user_id": 1,
            "sender_user_id": 2,
        }

        first_previous_task_model = Task(**first_previous_task)
        first_subsequent_task_model = Task(**first_subsequent_task)
        second_previous_task_model = Task(**second_previous_task)
        second_subsequent_task_model = Task(**second_subsequent_task)
        task_model = Task(**task_data)

        task_model.previous_tasks.append(first_previous_task_model)
        task_model.previous_tasks.append(second_previous_task_model)
        task_model.subsequent_tasks.append(first_subsequent_task_model)
        task_model.subsequent_tasks.append(second_subsequent_task_model)

        create_user(self.receiver_user)
        create_user(self.sender_user)

        db.session.add_all(
            [
                first_previous_task_model,
                second_previous_task_model,
                first_subsequent_task_model,
                second_subsequent_task_model,
                task_model,
            ]
        )
        db.session.commit()

        task = Task.query.filter_by(id=5).first()

        assert task.all_previous_tasks == Task.query.all()[:2]
        assert task.all_subsequent_tasks == Task.query.all()[2:4]
        check_model_fields(
            task,
            task_data,
            "time",
            "all_previous_tasks",
            "all_subsequent_tasks",
        )

    def test_current_task(self, client: FlaskClient):
        create_user(
            {
                "id": 5,
                "username": "username5",
            }
        )

        task = Task(
            id=6,
            title="Выполнить задание 3",
            time=datetime.now(),
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=4,
            sender_user_id=5,
        )

        user_data = {
            "id": 4,
            "username": "username4",
            "current_task_id": None,
        }

        db.session.add(TaskUser(**user_data))
        db.session.commit()

        db.session.add(task)
        db.session.commit()

        user_data["current_task_id"] = task.id
        TaskUser.query.filter_by(
            id=user_data["id"]
        ).first().current_task_id = user_data["current_task_id"]
        db.session.commit()

        check_model_fields(
            TaskUser.query.filter_by(id=user_data["id"]).first(),
            user_data,
        )
