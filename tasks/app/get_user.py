from .tasks_client import tasks_client
from models import TaskUser
from app.pb.tasks_pb2 import GetUserFromTokenRequest


def get_user(token: str):
    users_response = tasks_client.GetUserFromToken(GetUserFromTokenRequest(token=token))
    user = TaskUser.query.filter_by(username=users_response.username).first()
    return user
