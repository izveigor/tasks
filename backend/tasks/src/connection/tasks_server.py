import grpc
from concurrent import futures
from flask import Blueprint, current_app

from constants import TASKS_HOST
from .pb.tasks_pb2_grpc import TasksServicer, add_TasksServicer_to_server
from .pb.tasks_pb2 import UserResponse
from models import TaskUser, db


class TasksService(TasksServicer):
    def __init__(self, app):
        self.app = app

    def AddUser(self, request, context):
        with self.app.app_context():
            id_ = request.id
            username = request.username
            image = request.image

            user = TaskUser(
                id=id_,
                username=username,
                image=image,
            )

            db.session.add(user)
            db.session.commit()

            return UserResponse()

    def ChangeUser(self, request, context):
        with self.app.app_context():
            id_ = request.id
            username = request.username
            image = request.image

            user = TaskUser.query.get(id_)
            user.username = username
            user.image = image
            db.session.commit()

            return UserResponse()

    def DeleteUser(self, request, context):
        with self.app.app_context():
            id_ = request.id

            user = TaskUser.query.get(id_)
            db.session.delete(user)
            db.session.commit()

            return UserResponse()


def tasks_serve(app):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TasksServicer_to_server(TasksService(app), server)
    server.add_insecure_port(TASKS_HOST)
    server.start()
    server.wait_for_termination()
