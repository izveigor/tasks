from concurrent import futures
from typing import Any

import grpc
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from account.constants import USERS_HOST
from account.pb.users_pb2 import (
    AuthorizationRequest,
    AuthorizationResponse,
    PermissionRequest,
)
from account.pb.users_pb2_grpc import UsersServicer, add_UsersServicer_to_server
from users.models import ConfirmEmail


class UsersService(UsersServicer):  # type: ignore
    def CheckPermission(
        self, request: PermissionRequest, context: Any
    ) -> AuthorizationResponse:
        receiver_username = request.receiverUsername
        sender_token = request.senderToken

        receiver_user = User.objects.get(username=receiver_username)
        sender_user = User.objects.get(token=sender_token)

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

        return AuthorizationResponse(
            is_permission_exist=result,
            username=sender_user.username,
        )

    def AuthorizationLikeUser(
        self, request: AuthorizationRequest, context: Any
    ) -> AuthorizationResponse:
        token = request.token
        user = User.objects.get(token=token)
        email = user.confirm_email
        result = False
        if email.confirmed:  # type: ignore
            result = True

        return AuthorizationResponse(
            is_permission_exist=result,
            username=user.username,
        )

    def AuthorizationLikeTeammate(
        self, request: AuthorizationRequest, context: Any
    ) -> AuthorizationResponse:
        token = request.token
        user = User.objects.get(token=token)
        result = False
        if user.profile.team:
            result = True

        return AuthorizationResponse(
            is_permission_exist=result,
            username=user.username,
        )


def users_serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UsersServicer_to_server(UsersService(), server)
    server.add_insecure_port(USERS_HOST)
    server.start()
    server.wait_for_termination()
