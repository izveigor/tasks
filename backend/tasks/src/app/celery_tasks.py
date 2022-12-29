from typing import Any

from constants import TASK_STATUS
from models import Task

from .celery import celery
from .task_topological_sort import TaskTopologicalSort


@celery.task
def validate_task_data(
    task_json: dict[str, Any],
    previous_tasks: list[Task],
    subsequent_tasks: list[Task],
) -> bool:
    if task_json["receiver_user_id"] == task_json["sender_user_id"]:
        return False

    for previous_task in previous_tasks:
        if not (
            previous_task.receiver_user_id == task_json["receiver_user_id"]
            and previous_task.sender_user_id == task_json["sender_user_id"]
        ):
            return False

    for subsequent_task in subsequent_tasks:
        if not (
            subsequent_task.receiver_user_id == task_json["receiver_user_id"]
            and subsequent_task.sender_user_id == task_json["sender_user_id"]
        ):
            return False

    all_previous_tasks = TaskTopologicalSort().topological_sort(previous_tasks)
    all_subsequent_tasks = TaskTopologicalSort().topological_sort(subsequent_tasks)

    if set(previous_tasks) & set(all_subsequent_tasks):
        return False

    if set(subsequent_tasks) & set(all_previous_tasks):
        return False

    return True
