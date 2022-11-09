from .tasks_client import tasks_client
from app.pb.tasks_pb2 import PermissionRequest


def get_permission(receiver_username: str, sender_username: str) -> bool:
    users_response = tasks_client.CheckPermission(
        PermissionRequest(
            receiverUsername=receiver_username,
            senderUsername=sender_username,
        )
    )
    return users_response.is_permission_exist
