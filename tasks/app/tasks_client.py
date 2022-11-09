import grpc
from app.pb.tasks_pb2_grpc import TasksStub
from .constants import TASKS_HOST

tasks_channel = grpc.insecure_channel(TASKS_HOST)

tasks_client = TasksStub(tasks_channel)
