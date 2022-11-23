from unittest.mock import patch, Mock
from flask.testing import FlaskClient
from constants import TASK_STATUS, TASKS_NUMBER_FOR_PAGE, PREFIX_HOST, PROCESSING_TASK_STATUS
from tests.helpers import create_user, check_model_fields, create_receiver_and_sender_users
from models import TaskUser, Task, db
from datetime import datetime
from app.serializers import task_schema
import json
import uuid


class TestTaskView:
    @patch("app.views.authorization_like_user")
    def test_get(
        self,
        mock_authorization_like_user: Mock,
        client: FlaskClient,
    ):
        receiver_user, sender_user = create_receiver_and_sender_users()
        mock_authorization_like_user.return_value = ("11111", TaskUser.query.get(receiver_user["id"]))
        time = datetime.now()
        first_task = Task(
            id=1,
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        second_task = Task(
            id=2,
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        db.session.add_all(
            [
                first_task,
                second_task,
            ]
        )
        db.session.commit()

        response = client.get(PREFIX_HOST+"/task/1/")
        assert response.status == "200 OK"
        assert json.loads(response.data.decode("utf-8")) == {
            "id": first_task.id,
            "title": first_task.title,
            "description": first_task.description,
            "time": first_task.time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "status": first_task.status,
            "receiver_user": {"image": receiver_user["image"]}
        }

    @patch("app.views.authorization_like_teammate")
    @patch("app.views.validate_task_data.delay")
    def test_put(
        self,
        mock_validate_task_data: Mock,
        mock_authorization: Mock,
        client: FlaskClient,
    ):
        mock_validate_task_data.return_value.get.return_value = True
        receiver_user, sender_user = create_receiver_and_sender_users()
        mock_authorization.return_value = ("11111", TaskUser.query.get(sender_user["id"]))

        time = datetime.now()
        first_task = Task(
            id=1,
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        second_task = Task(
            id=2,
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        third_task = Task(
            id=3,
            title="Выполнить задание 3",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        db.session.add_all(
            [
                first_task,
                second_task,
                third_task,
            ]
        )
        db.session.commit()

        changed_previous_tasks = [first_task.id]
        changed_subsequent_tasks = [third_task.id]

        changed_task_data = {
            "title": "Выполнить новое задание 1",
            "time": datetime.now(),
            "description": "Нужно его выполнить.",
            "status": TASK_STATUS[1],
        }
        changed_task = Task(**changed_task_data)

        response = client.put(
            PREFIX_HOST+"/task/2/",
            data=json.dumps(
                {
                    **task_schema.dump(changed_task),
                    "previous_tasks_ids": changed_previous_tasks,
                    "subsequent_tasks_ids": changed_subsequent_tasks,
                },
            ),
            content_type="application/json",
        )

        assert response.status == "200 OK"

        changed_task_after_response = Task.query.get(2)

        assert changed_task_after_response.title == changed_task_data["title"]
        assert changed_task_after_response.time == changed_task_data["time"]
        assert (
            changed_task_after_response.description == changed_task_data["description"]
        )
        assert changed_task_after_response.status == changed_task_data["status"]

        assert changed_task_after_response.previous_tasks == [
            Task.query.get(id_) for id_ in changed_previous_tasks
        ]

        assert changed_task_after_response.subsequent_tasks == [
            Task.query.get(id_) for id_ in changed_subsequent_tasks
        ]

    @patch("app.views.authorization_like_teammate")
    def test_delete(
        self,
        mock_authorization: Mock,
        client: FlaskClient,
    ):
        receiver_user, sender_user = create_receiver_and_sender_users()
        mock_authorization.return_value = ("11111", TaskUser.query.get(sender_user["id"]))
        time = datetime.now()
        first_task = Task(
            id=1,
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        second_task = Task(
            id=2,
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        db.session.add_all(
            [
                first_task,
                second_task,
            ]
        )
        db.session.commit()

        response = client.delete(PREFIX_HOST+"/task/1/")

        assert response.status == "200 OK"
        assert Task.query.all() == [second_task]


@patch("app.views.authorization_like_teammate")
class TestCurrentTaskView:
    def test_get(
        self,
        mock_authorization: Mock,
        client: FlaskClient,
    ):
        receiver_user, sender_user = create_receiver_and_sender_users()
        mock_authorization.return_value = ("11111", TaskUser.query.get(receiver_user["id"]))

        time = datetime.now()
        first_task = Task(
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        second_task = Task(
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        db.session.add_all(
            [
                first_task,
                second_task,
            ]
        )
        db.session.commit()

        TaskUser.query.get(receiver_user["id"]).current_task = second_task
        db.session.commit()

        response = client.get(PREFIX_HOST+"/current_task/")

        assert response.status == "200 OK"
        assert json.loads(response.data.decode("utf-8")) == {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "description": "Описание отсутствует.",
            "title": "Выполнить задание 2",
            "status": TASK_STATUS[0],
            "receiver_user": {"image": "http://image1"},
            "id": 2,
        }

    @patch("app.views.TaskTopologicalSort.__init__", return_value=None)
    @patch("app.views.TaskTopologicalSort.next_task")
    def test_put(
        self,
        mock_get_next_task: Mock,
        mock_task_topological_sort__init__: Mock,
        mock_authorization: Mock,
        client: FlaskClient,
    ):
        receiver_user, sender_user = create_receiver_and_sender_users()
        mock_authorization.return_value = ("11111", TaskUser.query.get(receiver_user["id"]))

        time = datetime.now()
        first_task = Task(
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        second_task = Task(
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        db.session.add_all(
            [
                first_task,
                second_task,
            ]
        )
        TaskUser.query.get(receiver_user["id"]).current_task = first_task
        db.session.commit()

        mock_get_next_task.return_value = Task.query.get(2)

        response = client.put(PREFIX_HOST+"/current_task/")

        assert response.status == "200 OK"
        assert TaskUser.query.get(receiver_user["id"]).current_task == second_task


@patch("app.views.authorization_like_teammate")
class TestProcessingView:
    def test_get(
        self,
        mock_authorization: Mock,
        client: FlaskClient,
    ):
        receiver_user, sender_user = create_receiver_and_sender_users()
        mock_authorization.return_value = ("11111", TaskUser.query.get(receiver_user["id"]))

        time = datetime.now()
        first_task = Task(
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=PROCESSING_TASK_STATUS,
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        db.session.add(first_task)

        response = client.get(PREFIX_HOST+"/processing/")
        assert response.status == "200 OK"


class TestTasksView:
    @patch("app.views.authorization_like_user")
    def test_get(
        self,
        mock_authorization: Mock,
        client: FlaskClient,
    ):
        receiver_user, sender_user = create_receiver_and_sender_users()
        mock_authorization.return_value = ("11111", TaskUser.query.get(receiver_user["id"]))

        time = datetime.now()
        tasks = [Task(
                id=id_,
                title=str(id_),
                time=time,
                description="Описание отсутствует.",
                status=TASK_STATUS[0],
                receiver_user_id=receiver_user["id"],
                sender_user_id=sender_user["id"],
        ) for id_ in range(1, 24)]

        db.session.add_all(tasks)
        db.session.commit()

        response_with_first_page = client.get(PREFIX_HOST+"/tasks/?page=1",)

        first_json_tasks = json.loads(response_with_first_page.data.decode("utf-8"))
        assert len(first_json_tasks) == TASKS_NUMBER_FOR_PAGE
        for id_, json_task in enumerate(first_json_tasks, start=1):
            assert json_task["title"] == str(id_)

        response_with_second_page = client.get(PREFIX_HOST+"/tasks/?page=2")

        second_json_tasks = json.loads(response_with_second_page.data.decode("utf-8"))
        assert len(second_json_tasks) == TASKS_NUMBER_FOR_PAGE
        for id_, json_task in enumerate(second_json_tasks, start=11):
            assert json_task["title"] == str(id_)

    @patch("app.views.authorization_like_teammate")
    @patch("app.views.NotificationRequest")
    @patch("app.views.notifications_client.Notify")
    @patch("app.views.get_permission")
    @patch("app.views.validate_task_data.delay")
    def test_post(
        self,
        mock_validate_task_data: Mock,
        mock_get_permission: Mock,
        mock_notifications_client_Notify: Mock,
        mock_NotificationRequest: Mock,
        mock_authorization: Mock,
        client: FlaskClient,
    ):
        mock_get_permission.return_value = True
        mock_validate_task_data.return_value.get.return_value = True
        receiver_user, sender_user = create_receiver_and_sender_users()
        mock_authorization.return_value = ("11111", TaskUser.query.get(sender_user["id"]))

        time = datetime.now()
        first_task = Task(
            title="Выполнить задание 1",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        second_task = Task(
            title="Выполнить задание 2",
            time=time,
            description="Описание отсутствует.",
            status=TASK_STATUS[0],
            receiver_user_id=receiver_user["id"],
            sender_user_id=sender_user["id"],
        )

        db.session.add_all(
            [
                first_task,
                second_task,
            ]
        )
        db.session.commit()

        previous_tasks_ids = [first_task.id]
        subsequent_tasks_ids = [second_task.id]

        response = client.post(
            PREFIX_HOST+"/tasks/",
            data=json.dumps(
                {
                    "title": "Задание",
                    "time": "17:00",
                    "description": "Описание отсутствует.",
                    "receiver_username": receiver_user["username"],
                    "previous_tasks_ids": previous_tasks_ids,
                    "subsequent_tasks_ids": subsequent_tasks_ids,
                },
                default=str,
            ),
            content_type="application/json",
        )

        assert response.status == "201 CREATED"

        created_task = Task.query.get(3)

        assert created_task.all_previous_tasks == [first_task]
        assert created_task.all_subsequent_tasks == [second_task]

        check_model_fields(
            created_task,
            {
                "id": 3,
                "title": "Задание",
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": receiver_user["id"],
                "sender_user_id": sender_user["id"],
            },
            "time",
            "all_previous_tasks",
            "all_subsequent_tasks",
        )
