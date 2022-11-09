from .tasks_client import tasks_client
from app.pb.tasks_pb2 import ConfirmEmailRequest


def get_email_permission(username: str):
    users_response = tasks_client.ConfirmEmail(
        ConfirmEmailRequest(
            username=username,
        )
    )
    return users_response.is_permission_exist
