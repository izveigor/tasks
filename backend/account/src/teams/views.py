from django.contrib.auth import get_user_model
from google.protobuf.timestamp_pb2 import Timestamp  # type: ignore
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.notifications_client import notifications_client  # type: ignore
from account.pb.notifications_pb2 import NotificationRequest
from account.permissions import (
    AdminTeamPermission,
    CreatorTeamPermission,
    EmailPermission,
    TeamPermission,
)
from users.serializers import UsernameSerializer

from . import serializers
from .models import Team

User = get_user_model()


class AuthorizationLikeTeammate(APIView):  # type: ignore
    permission_classes = [IsAuthenticated, EmailPermission, TeamPermission]

    def get(self, request, format=None) -> Response:
        return Response(status=status.HTTP_200_OK)


class AuthorizationLikeAdmin(APIView):  # type: ignore
    permission_classes = [IsAuthenticated, EmailPermission, AdminTeamPermission]

    def get(self, request, format=None) -> Response:
        return Response(status=status.HTTP_200_OK)


class AuthorizationLikeCreator(APIView):  # type: ignore
    permission_classes = [IsAuthenticated, EmailPermission, CreatorTeamPermission]

    def get(self, request, format=None) -> Response:
        return Response(status=status.HTTP_200_OK)


class CheckTeamNameView(APIView):  # type: ignore
    def post(self, request, format=None) -> Response:
        serializer = serializers.TeamNameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        name = serializer.validated_data["name"]
        response = {}
        if Team.objects.filter(name=name).exists():
            response["exist"] = True
        else:
            response["exist"] = False

        return Response(response, status=status.HTTP_200_OK)


class TeamView(APIView):  # type: ignore
    permission_classes = [IsAuthenticated, EmailPermission, AdminTeamPermission]

    def get(self, request, format=None) -> Response:
        serializer = serializers.TeamSerializer(request.team)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None) -> Response:
        request.team.name = self.request.data["name"]
        request.team.description = self.request.data["description"]
        request.team.image = self.request.data["image"]
        request.team.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None) -> Response:
        for profile in request.team.users.all():
            profile.supervisor = None
            profile.save()

        request.team.delete()
        return Response(status=status.HTTP_200_OK)


class JoinTeamView(APIView):  # type: ignore
    permission_classes = [IsAuthenticated, EmailPermission]

    def put(self, request, format=None) -> Response:
        serializer = serializers.TeamNameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data["name"]

        try:
            team = Team.objects.get(name=name)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        token = Token.objects.get(user=team.admin)

        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        notifications_client.Notify(
            NotificationRequest(
                text=f'Пользователь "{self.request.user.username}" хочет присоединиться к вашей команде.',
                image=self.request.user.profile.image.url,
                time=timestamp,
                tokens=[token.key],
            )
        )

        return Response(status=status.HTTP_200_OK)


class AcceptIntoTeamView(APIView):  # type: ignore
    permission_classes = [IsAuthenticated, EmailPermission]

    def put(self, request, format=None) -> Response:
        try:
            team = Team.objects.get(admin=self.request.user)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = UsernameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.profile.team = team
        user.save()

        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        token = Token.objects.get(user=user)
        notifications_client.Notify(
            NotificationRequest(
                text=f'Вы присоединились к команде "{team.name}".',
                image=team.image.url,
                time=timestamp,
                tokens=[token.key],
            )
        )

        return Response(status=status.HTTP_200_OK)


class SuggestTeamView(APIView):  # type: ignore
    permission_classes = [IsAuthenticated, EmailPermission]

    def post(self, request, format=None) -> Response:
        serializer = serializers.TeamNameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data["name"]
        try:
            team = Team.objects.get(name__icontains=name)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        team_serializer = serializers.TeamSerializer(team)
        return Response(team_serializer.data, status=status.HTTP_200_OK)


class TeamsView(APIView):  # type: ignore
    permission_classes = [IsAuthenticated, EmailPermission]

    def post(self, request, format=None) -> Response:
        if self.request.user.profile.team:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.TeamSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        team = Team.objects.create(
            **serializer.data,
            admin=self.request.user,
        )

        self.request.user.profile.team = team
        self.request.user.profile.save()

        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        notifications_client.Notify(
            NotificationRequest(
                text=f'Команда "{team.name}" была успешна создана.',
                image=self.request.user.profile.image.url,
                time=timestamp,
                tokens=[str(self.request.auth)],
            )
        )

        return Response(status=status.HTTP_201_CREATED)


class LeaveTeamView(APIView):  # type: ignore
    permission_classes = [IsAuthenticated, EmailPermission, TeamPermission]

    def put(self, request, format=None) -> Response:
        self.request.user.profile.team = None
        self.request.user.profile.save()
        return Response(status=status.HTTP_200_OK)
