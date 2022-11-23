from connection.pb.users_pb2 import AuthorizationRequest, PermissionRequest
from connection.users_client import users_client
from flask import Request
from models import TaskUser


def get_token(auth_header) -> str:
    if auth_header:
        auth_arguments = auth_header.split(" ")
        auth_name = auth_arguments[0]
        if auth_name == "Token":
            auth_token = auth_arguments[1]
        else:
            auth_token = ""
    else:
        auth_token = ""

    return auth_token


def authorization_like_user(request: Request) -> tuple[str, TaskUser]:
    auth_headers = request.headers.get("Authorization")
    token = get_token(auth_headers)
    if not token:
        raise ValueError()
    else:
        users_response = users_client.AuthorizationLikeTeammate(
            AuthorizationRequest(
                token=token,
            )
        )
        users_response.is_permission_exist
        if users_response.is_permission_exist:
            user = TaskUser.query.filter_by(
                username=users_response.username,
            ).first()
            return (token, user)
        else:
            raise ValueError()


def authorization_like_teammate(request: Request) -> tuple[str, TaskUser]:
    auth_headers = request.headers.get("Authorization")
    token = get_token(auth_headers)
    if not token:
        raise ValueError()
    else:
        users_response = users_client.AuthorizationLikeTeammate(
            AuthorizationRequest(
                token=token,
            )
        )
        users_response.is_permission_exist
        if users_response.is_permission_exist:
            user = TaskUser.query.filter_by(
                username=users_response.username,
            ).first()
            return (token, user)
        else:
            raise ValueError()


def get_permission(request: Request, receiver_username: str) -> tuple[str, TaskUser]:
    auth_headers = request.headers.get("Authorization")
    token = get_token(auth_headers)
    if not token:
        raise ValueError()
    else:
        users_response = users_client.CheckPermission(
            PermissionRequest(
                receiverUsername=receiver_username,
                senderToken=token,
            )
        )
        if users_response.is_permission_exist:
            user = TaskUser.query.filter_by(
                username=users_response.username,
            ).first()
            return (token, user)
        else:
            raise ValueError()
