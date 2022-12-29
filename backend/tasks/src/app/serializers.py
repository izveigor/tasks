from flask import Blueprint
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

from models import Task, TaskUser

bp_marhmallow = Blueprint("marhmallow", __name__)
ma = Marshmallow(bp_marhmallow)


class TaskUserSchema(ma.Schema):  # type: ignore
    class Meta:
        model = TaskUser
        fields = ("image",)


class TaskSchema(ma.Schema):  # type: ignore
    class Meta:
        model = Task
        fields = (
            "id",
            "status",
            "title",
            "time",
            "description",
            "receiver_user",
        )

    receiver_user = ma.Nested(TaskUserSchema)


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
