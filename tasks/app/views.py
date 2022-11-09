from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, reqparse
from app.constants import TASKS_NUMBER_FOR_PAGE, PROCESSING_TASK_STATUS
from .authorization import authorization
from .get_permission import get_permission
from models import db, Task, TaskUser
from .serializers import task_schema, tasks_schema
from .celery_tasks import validate_task_data
from .notifications_client import notifications_client
from app.pb.notifications_pb2 import NotificationRequest
from .task_topological_sort import TaskTopologicalSort
import datetime


bp_views = Blueprint("views", __name__)
api = Api(bp_views)


class TaskView(Resource):
    def get(self, task_id: int):
        task = Task.query.filter_by(id=task_id).first()
        if task is None:
            return "not found", 404

        try:
            _, user = authorization(request)
        except ValueError:
            return "unauthorized", 401

        return task_schema.dump(task)

    def put(self, task_id: int):
        task = Task.query.filter_by(id=task_id).first()
        if task is None:
            return "not found", 404

        try:
            _, sender_user = authorization(request)
        except ValueError:
            return "unauthorized", 401

        if task.receiver_user.current_task == task:
            return "bad request", 400

        if task.sender_user_id == sender_user.id:
            previous_tasks = [
                Task.query.get(id_) for id_ in request.json["previous_tasks_ids"]
            ]

            subsequent_tasks = [
                Task.query.get(id_) for id_ in request.json["subsequent_tasks_ids"]
            ]

            task_json = {
                "title": request.json["title"],
                "time": request.json["time"],
                "description": request.json["description"],
                "status": request.json["status"],
                "receiver_user": task.receiver_user,
                "sender_user": sender_user,
            }

            result = validate_task_data.delay(
                task_json, previous_tasks, subsequent_tasks
            )

            is_task_data_right = result.get()
            if is_task_data_right:

                task.title = task_json["title"]
                task.time = task_json["time"]
                task.description = task_json["description"]
                task.status = task_json["status"]

                task.previous_tasks = previous_tasks
                task.subsequent_tasks = subsequent_tasks

                db.session.add(task)
                db.session.commit()
            else:
                return "bad request", 400
        else:
            return "unauthorized", 401

    def delete(self, task_id):
        task = Task.query.filter_by(id=task_id).first()
        if task is None:
            return "not found", 404

        try:
            _, sender_user = authorization(request)
        except ValueError:
            return "unauthorized", 401

        if task.sender_user_id == sender_user.id:
            db.session.delete(task)
            db.session.commit()
        else:
            return "unauthorized", 401


class CurrentTaskView(Resource):
    def get(self):
        try:
            _, user = authorization(request)
        except ValueError:
            return "unauthorized", 401

        current_task = task_schema.dump(user.current_task)
        if current_task:
            return current_task
        else:
            return "bad request", 400

    def put(self):
        try:
            _, user = authorization(request)
        except ValueError:
            return "unauthorized", 401

        tasks = Task.query.filter_by(
            receiver_user_id=user.id,
            status=PROCESSING_TASK_STATUS,
        ).all()

        next_task = TaskTopologicalSort().next_task(tasks, user.id)

        user.current_task_id = next_task.id
        db.session.commit()
        return "ok", 200


class ProcessingView(Resource):
    def get(self):
        try:
            _, user = authorization(request)
        except ValueError:
            return "unauthorized", 401

        tasks = Task.query.filter(
            (Task.receiver_user_id == user.id) & (Task.status == PROCESSING_TASK_STATUS)
        ).all()
        if tasks:
            return "ok", 200
        else:
            return "bad request", 400


class TasksView(Resource):
    def get(self):
        page = request.args.get("page", type=int)
        try:
            _, user = authorization(request)
        except ValueError:
            return "unauthorized", 401

        page = request.args.get("page", type=int)
        if page == 0:
            return "bad request", 400

        tasks = tasks_schema.dump(
            Task.query.filter(
                (Task.receiver_user_id == user.id) | (Task.sender_user_id == user.id)
            ).all()[
                ((page - 1) * TASKS_NUMBER_FOR_PAGE) : (page * TASKS_NUMBER_FOR_PAGE)
            ]
        )
        if tasks:
            return tasks
        else:
            return "bad request", 400

    def post(self):
        try:
            token, sender_user = authorization(request)
        except ValueError:
            return "unauthorized", 401

        receiver_username = request.json["receiver_username"]
        is_permission_exist = get_permission(
            receiver_username,
            sender_user.username,
        )

        if is_permission_exist:
            previous_tasks = [
                Task.query.get(id_) for id_ in request.json["previous_tasks_ids"]
            ]

            subsequent_tasks = [
                Task.query.get(id_) for id_ in request.json["subsequent_tasks_ids"]
            ]

            time = request.json["time"].split(":")
            timedelta = datetime.timedelta(
                hours=int(time[0]),
                minutes=int(time[1]),
            )

            task_json = {
                "title": request.json["title"],
                "time": datetime.datetime.now() + timedelta,
                "description": request.json["description"],
                "receiver_user_id": TaskUser.query.filter_by(username=receiver_username)
                .first()
                .id,
                "sender_user_id": sender_user.id,
            }

            result = validate_task_data.delay(
                task_json, previous_tasks, subsequent_tasks
            )
            is_task_data_right = result.get()
            if is_task_data_right:
                task = Task(**task_json)
                task.previous_tasks = previous_tasks
                task.subsequent_tasks = subsequent_tasks

                db.session.add(task)
                db.session.commit()

                notifications_client.Notify(
                    NotificationRequest(
                        text=f'Пользователь "{sender_user.username}" создал задание для пользователя "{receiver_username}".',
                        image=sender_user.image,
                        time=datetime.datetime.now(),
                        tokens=[token],
                    )
                )

                return "created", 201
            else:
                return "bad request", 400
        else:
            return "unauthorized", 401


class TaskClose(Resource):
    def put(self):
        try:
            _, user = authorization(request)
        except ValueError:
            return "unauthorized", 401

        status = request.json["status"]

        current_task = user.current_task
        current_task.status = status
        user.current_task = None
        db.session.commit()

        return "ok", 200


api.add_resource(TaskView, "/task/<int:task_id>/")
api.add_resource(CurrentTaskView, "/current_task/")
api.add_resource(TasksView, "/tasks/")
api.add_resource(ProcessingView, "/processing/")
api.add_resource(TaskClose, "/close/")
