import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref

from constants import DEFAULT_TASK_STATUS, TASK_STATUS

db = SQLAlchemy()


previous_task = db.Table(
    "previous_tasks",
    db.Column(
        "previous_task_id", db.Integer, db.ForeignKey("task.id"), primary_key=True
    ),
    db.Column("task_id", db.Integer, db.ForeignKey("task.id"), primary_key=True),
)

subsequent_task = db.Table(
    "subsequent_tasks",
    db.Column("subsequent_task_id", db.Integer, db.ForeignKey("task.id")),
    db.Column("task_id", db.Integer, db.ForeignKey("task.id")),
)


class TaskUser(db.Model):  # type: ignore
    __tablename__ = "task_user"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(150), nullable=False, unique=True)
    image = db.Column(db.String(150), nullable=False)
    current_task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=True)

    current_task = db.relationship(
        "Task",
        foreign_keys=[current_task_id],
    )


class Task(db.Model):  # type: ignore
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum(*TASK_STATUS, name="status"),
        nullable=False,
        default=DEFAULT_TASK_STATUS,
    )

    receiver_user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("task_user.id"), nullable=False
    )
    sender_user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("task_user.id"), nullable=False
    )
    receiver_user = db.relationship("TaskUser", foreign_keys=[receiver_user_id])
    sender_user = db.relationship("TaskUser", foreign_keys=[sender_user_id])

    previous_tasks = db.relationship(
        "Task",
        secondary=previous_task,
        primaryjoin=id == previous_task.c.previous_task_id,
        secondaryjoin=id == previous_task.c.task_id,
    )

    subsequent_tasks = db.relationship(
        "Task",
        secondary=subsequent_task,
        primaryjoin=id == subsequent_task.c.subsequent_task_id,
        secondaryjoin=id == subsequent_task.c.task_id,
    )


previous_task_union = (
    db.select(
        [
            previous_task.c.previous_task_id,
            previous_task.c.task_id,
        ]
    )
    .union(
        db.select(
            [
                previous_task.c.previous_task_id,
                previous_task.c.task_id,
            ]
        )
    )
    .alias()
)

subsequent_tasks_union = (
    db.select(
        [
            subsequent_task.c.subsequent_task_id,
            subsequent_task.c.task_id,
        ]
    )
    .union(
        db.select(
            [
                subsequent_task.c.subsequent_task_id,
                subsequent_task.c.task_id,
            ]
        )
    )
    .alias()
)

Task.all_previous_tasks = db.relationship(
    "Task",
    secondary=previous_task_union,
    primaryjoin=Task.id == previous_task_union.c.previous_task_id,
    secondaryjoin=Task.id == previous_task_union.c.task_id,
    viewonly=True,
)

Task.all_subsequent_tasks = db.relationship(
    "Task",
    secondary=subsequent_tasks_union,
    primaryjoin=Task.id == subsequent_tasks_union.c.subsequent_task_id,
    secondaryjoin=Task.id == subsequent_tasks_union.c.task_id,
    viewonly=True,
)
