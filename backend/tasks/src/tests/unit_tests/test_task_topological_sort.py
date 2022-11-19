'''from app.task_topological_sort import TaskTopologicalSort
from constants import TASK_STATUS, PROCESSING_TASK_STATUS
from datetime import datetime
from tests.helpers import create_user
from models import Task, db
from flask.testing import FlaskClient


class TestTaskTopologicalSort:
    def test_task_topological_sort(self, client: FlaskClient):
        create_user(
            {
                "id": 11,
                "username": "username11",
                "current_task_id": None,
            }
        )
        create_user(
            {
                "id": 12,
                "username": "username12",
                "current_task_id": None,
            }
        )
        create_user(
            {
                "id": 13,
                "username": "username13",
                "current_task_id": None,
            }
        )

        not_processing_tasks = list(TASK_STATUS)
        not_processing_tasks.remove(PROCESSING_TASK_STATUS)

        first_task = Task(
            **{
                "id": 11,
                "title": "Выполнить задание 1",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": not_processing_tasks[0],
                "receiver_user_id": 11,
                "sender_user_id": 12,
            }
        )
        second_task = Task(
            **{
                "id": 12,
                "title": "Выполнить задание 2",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": 11,
                "sender_user_id": 13,
            }
        )
        third_task = Task(
            **{
                "id": 13,
                "title": "Выполнить задание 3",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": 11,
                "sender_user_id": 13,
            }
        )
        fourth_task = Task(
            **{
                "id": 14,
                "title": "Выполнить задание 4",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": not_processing_tasks[0],
                "receiver_user_id": 11,
                "sender_user_id": 12,
            }
        )
        fifth_task = Task(
            **{
                "id": 15,
                "title": "Выполнить задание 5",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": 11,
                "sender_user_id": 12,
            }
        )
        sixth_task = Task(
            **{
                "id": 16,
                "title": "Выполнить задание 6",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": not_processing_tasks[0],
                "receiver_user_id": 11,
                "sender_user_id": 13,
            }
        )
        seventh_task = Task(
            **{
                "id": 17,
                "title": "Выполнить задание 7",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": 11,
                "sender_user_id": 12,
            }
        )
        eighth_task = Task(
            **{
                "id": 18,
                "title": "Выполнить задание 7",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": 11,
                "sender_user_id": 12,
            }
        )
        nineth_task = Task(
            **{
                "id": 19,
                "title": "Выполнить задание 7",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": 11,
                "sender_user_id": 12,
            }
        )

        second_task.subsequent_tasks.append(fifth_task)
        third_task.subsequent_tasks.append(fifth_task)

        fifth_task.previous_tasks.append(second_task)
        fifth_task.previous_tasks.append(third_task)

        fifth_task.subsequent_tasks.append(seventh_task)
        fifth_task.subsequent_tasks.append(eighth_task)

        seventh_task.subsequent_tasks.append(fifth_task)
        eighth_task.subsequent_tasks.append(fifth_task)

        eighth_task.subsequent_tasks.append(nineth_task)
        nineth_task.subsequent_tasks.append(eighth_task)

        db.session.add_all(
            [
                first_task,
                second_task,
                third_task,
                fourth_task,
                fifth_task,
                sixth_task,
                seventh_task,
                eighth_task,
                nineth_task,
            ]
        )
        db.session.commit()

        assert TaskTopologicalSort().topological_sort(
            Task.query.filter_by(
                receiver_user_id=11,
                status=PROCESSING_TASK_STATUS,
            ).all()
        ) == [
            third_task,
            second_task,
            fifth_task,
            eighth_task,
            nineth_task,
            seventh_task,
        ]

        assert TaskTopologicalSort().next_task(11) == third_task
'''