import uuid
from datetime import datetime

from flask.testing import FlaskClient

from app.task_topological_sort import TaskTopologicalSort
from constants import PROCESSING_TASK_STATUS, TASK_STATUS
from models import Task, db
from tests.helpers import create_user


class TestTaskTopologicalSort:
    def test_task_topological_sort(self, client: FlaskClient) -> None:
        uuids = [uuid.uuid4() for _ in range(3)]
        for i in range(3):
            create_user(
                {
                    "id": uuids[i],
                    "username": "username" + str(i),
                    "image": "http://image" + str(i),
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
                "receiver_user_id": uuids[0],
                "sender_user_id": uuids[1],
            }
        )
        second_task = Task(
            **{
                "id": 12,
                "title": "Выполнить задание 2",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": uuids[0],
                "sender_user_id": uuids[2],
            }
        )
        third_task = Task(
            **{
                "id": 13,
                "title": "Выполнить задание 3",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": uuids[0],
                "sender_user_id": uuids[2],
            }
        )
        fourth_task = Task(
            **{
                "id": 14,
                "title": "Выполнить задание 4",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": not_processing_tasks[0],
                "receiver_user_id": uuids[0],
                "sender_user_id": uuids[1],
            }
        )
        fifth_task = Task(
            **{
                "id": 15,
                "title": "Выполнить задание 5",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": uuids[0],
                "sender_user_id": uuids[1],
            }
        )
        sixth_task = Task(
            **{
                "id": 16,
                "title": "Выполнить задание 6",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": not_processing_tasks[0],
                "receiver_user_id": uuids[0],
                "sender_user_id": uuids[2],
            }
        )
        seventh_task = Task(
            **{
                "id": 17,
                "title": "Выполнить задание 7",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": uuids[0],
                "sender_user_id": uuids[1],
            }
        )
        eighth_task = Task(
            **{
                "id": 18,
                "title": "Выполнить задание 7",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": uuids[0],
                "sender_user_id": uuids[1],
            }
        )
        nineth_task = Task(
            **{
                "id": 19,
                "title": "Выполнить задание 7",
                "time": datetime.now(),
                "description": "Описание отсутствует.",
                "status": PROCESSING_TASK_STATUS,
                "receiver_user_id": uuids[0],
                "sender_user_id": uuids[1],
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
                receiver_user_id=uuids[0],
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

        assert TaskTopologicalSort().next_task(uuids[0]) == third_task
