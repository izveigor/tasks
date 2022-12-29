import grpc

from account.constants import TASKS_HOST
from account.pb.tasks_pb2_grpc import TasksStub

tasks_channel = grpc.insecure_channel(TASKS_HOST)

tasks_client = TasksStub(tasks_channel)
