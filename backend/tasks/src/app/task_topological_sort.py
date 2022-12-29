import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from sqlalchemy import or_

from constants import PROCESSING_TASK_STATUS
from models import Task, TaskUser, db


class Color(Enum):
    WHITE = 1
    GRAY = 2
    BLACK = 3


@dataclass(init=True, repr=False, eq=True, frozen=False)
class Node:
    task: Task
    color: Color
    time: int
    was_opened: int
    was_closed: int


class TaskTopologicalSort:
    time: int
    result: list[Task]

    def __init__(self) -> None:
        self.time = 0
        self.result = []

    @staticmethod
    def _search_node(nodes: list[Node], task: Task) -> Node:
        for node in nodes:
            if node.task == task:
                return node

        return nodes[0]

    def _DFS_visit(self, nodes: list[Node], u: Node) -> None:
        self.time += 1
        u.was_opened = self.time
        u.color = Color.GRAY
        subsequent_nodes = [
            self._search_node(nodes, task) for task in u.task.all_subsequent_tasks
        ]
        for v in subsequent_nodes:
            if v.color == Color.WHITE:
                self._DFS_visit(nodes, v)

        u.color = Color.BLACK
        self.time += 1
        u.was_closed = self.time
        self.result.append(u.task)

    def _DFS(self, nodes: list[Node]) -> None:
        for u in nodes:
            if u.color == Color.WHITE:
                self._DFS_visit(nodes, u)

    def topological_sort(self, tasks: list[Task]) -> list[Task]:
        nodes = [
            Node(
                task=task,
                color=Color.WHITE,
                time=0,
                was_opened=0,
                was_closed=0,
            )
            for task in tasks
        ]
        self._DFS(nodes)
        return self.result[::-1]

    def next_task(self, id_: Any) -> Task:
        tasks = Task.query.filter_by(
            receiver_user_id=id_,
            status=PROCESSING_TASK_STATUS,
        ).all()
        return self.topological_sort(tasks)[0]
