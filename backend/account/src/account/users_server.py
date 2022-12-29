from concurrent import futures
from typing import Any

import grpc
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from account.constants import USERS_HOST
from account.pb.users_pb2 import (
    ConfirmEmailRequest,
    ConfirmEmailResponse,
    GetTokenFromUsernameRequest,
    GetTokenFromUsernameResponse,
    GetUserFromTokenRequest,
    GetUserFromTokenResponse,
    PermissionRequest,
    PermissionResponse,
)
from account.pb.users_pb2_grpc import UsersServicer, add_UsersServicer_to_server
from users.models import ConfirmEmail


class UsersService(UsersServicer):  # type: ignore
    def CheckPermission(
        self, request: PermissionRequest, context: Any
    ) -> PermissionResponse:
        receiver_username = request.receiverUsername
        sender_username = request.senderUsername

        receiver_user = User.objects.get(username=receiver_username)
        sender_user = User.objects.get(username=sender_username)

        if receiver_user.profile.team == sender_user.profile.team:
            team = receiver_user.profile.team
            if sender_user == team.admin:
                result = True
            else:
                subordinates = sender_user.profile.get_subordinates()
                if receiver_user in subordinates:
                    result = True
                else:
                    result = False
        else:
            result = False

        return PermissionResponse(
            is_permission_exist=result,
        )

    def GetTokenFromUsername(
        self, request: GetTokenFromUsernameRequest, context: Any
    ) -> GetTokenFromUsernameResponse:
        username = request.username
        user = User.objects.get(username=username)
        token = Token.objects.get(user=user)

        return GetTokenFromUsernameResponse(
            token=token,
        )

    def GetUserFromToken(
        self, request: GetUserFromTokenRequest, context: Any
    ) -> GetUserFromTokenResponse:
        token = request.token
        user = Token.objects.get(key=token).user

        return GetUserFromTokenResponse(
            username=user.username,
        )

    def ConfirmEmail(
        self, request: ConfirmEmailRequest, context: Any
    ) -> ConfirmEmailResponse:
        username = request.username
        user = User.objects.get(username=username)
        confirm = ConfirmEmail.objects.get(user=user)

        if user.profile.team:
            result = confirm.confirmed
        else:
            result = False
        return ConfirmEmailResponse(
            is_permission_exist=result,
        )


def tasks_serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port(USERS_HOST)
    server.start()
    server.wait_for_termination()
