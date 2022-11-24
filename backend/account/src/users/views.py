from users.methods import suggest_username
from users.serializers import UserSerializer
from .models import Team, ConfirmEmail, Profile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from . import serializers
from rest_framework import permissions
from rest_framework import generics
from rest_framework.authtoken.models import Token
from .methods import suggest_username
import datetime
from django.utils import timezone
import random
from django.core.mail import send_mail
from django.conf import settings
from .permissions import (
    EmailPermission,
    AdminTeamPermission,
    TeamPermission,
    CreatorTeamPermission,
)
from .notifications_client import notifications_client
from .users_client import users_client
from account.pb.notifications_pb2 import NotificationRequest
import json
from account.constants import DEFAULT_PROFILE_IMAGE
from django.db.models import Q
from google.protobuf.timestamp_pb2 import Timestamp
from rest_framework.authtoken.models import Token
from account.tasks_client import tasks_client
from account.pb.tasks_pb2 import UserRequest
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginView(APIView):
    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = Token.objects.get_or_create(user=user)
        return Response({"token": token[0].key}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = serializers.RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = Token.objects.create(user=user)
        code = ""
        for _ in range(6):
            code += str(random.randint(0, 9))

        ConfirmEmail.objects.create(
            code=code,
            user=user,
        )

        Profile.objects.create(
            user=user,
        )

        tasks_client.AddUser(
            UserRequest(
                id=str(user.id),
                image=user.profile.image.url,
                username=user.username,
            )
        )

        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        notifications_client.Notify(
            NotificationRequest(
                text="Вы успешно зарегистрировались.",
                image=user.profile.image.url,
                time=timestamp,
                tokens=[token.key],
            )
        )

        send_mail(
            "Подтверждение email",
            f"Введите этот код: {code}",
            settings.EMAIL_HOST_USER,
            [user.email],
        )

        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def put(self, request, format=None):
        serializer = serializers.ChangePasswordSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]
        self.request.user.set_password(password)
        self.request.user.save()

        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        notifications_client.Notify(
            NotificationRequest(
                text="Пароль был успешно изменен.",
                image=self.request.user.profile.image.url,
                time=timestamp,
                tokens=[str(self.request.auth)],
            )
        )

        return Response(None, status.HTTP_200_OK)


class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def put(self, request, format=None):
        serializer = serializers.ChangeUsernameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        self.request.user.username = username
        self.request.user.save()

        tasks_client.ChangeUser(
            UserRequest(
                id=str(self.request.user.id),
                image=self.request.user.profile.image.url,
                username=self.request.user.username,
            )
        )

        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        notifications_client.Notify(
            NotificationRequest(
                text="Имя пользователя было успешно изменено.",
                image=self.request.user.profile.image.url,
                time=timestamp,
                tokens=[str(self.request.auth)],
            )
        )

        return Response(None, status.HTTP_200_OK)


class CheckUsernameView(APIView):
    def post(self, request, format=None):
        serializer = serializers.UsernameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        username = serializer.data["username"]
        response = {}
        if User.objects.filter(username=username).exists():
            response["exist"] = True
            response["available"] = suggest_username(username)
        else:
            response["exist"] = False

        return Response(response, status=status.HTTP_200_OK)

'''
class CheckAuthorization(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class CheckAuthorizationWithEmail(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class CheckCreatorView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, CreatorTeamPermission]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvatarView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def get(self, request, format=None):
        serializer = serializers.AvatarSerializer(self.request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        profile = user.profile
        serializer = serializers.ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SettingsProfileView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def get(self, request, format=None):
        profile = self.request.user.profile
        serializer = serializers.ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        profile = self.request.user.profile
        profile.job_title = self.request.data["job_title"]
        profile.description = self.request.data["description"]
        profile.image = self.request.data["image"]
        profile.save()

        self.request.user.first_name = self.request.data["first_name"]
        self.request.user.last_name = self.request.data["last_name"]
        self.request.user.save()

        users_client.ChangeUser(
            UserRequest(
                id=self.request.user.id,
                image=self.request.user.profile.image.url,
                username=self.request.user.username,
            )
        )

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        user = self.request.user
        user_id = user.id
        user.delete()

        users_client.DeleteUser(
            UserRequest(
                id=user_id,
            )
        )
        return Response(status=status.HTTP_200_OK)


class CheckEmailView(APIView):
    def post(self, request, format=None):
        serializer = serializers.CheckEmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        email = serializer.data["email"]
        response = {}
        if User.objects.filter(email=email).exists():
            response["exist"] = True
        else:
            response["exist"] = False

        return Response(response, status=status.HTTP_200_OK)


class CheckTeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, TeamPermission]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class CheckAdminTeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, AdminTeamPermission]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class CheckCreatorTeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, CreatorTeamPermission]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class TeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, AdminTeamPermission]

    def get(self, request, format=None):
        team = request.team
        serializer = serializers.CreateTeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        request.team.name = self.request.data["name"]
        request.team.description = self.request.data["description"]
        request.team.image = self.request.data["image"]
        request.team.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        request.team.delete()
        return Response(status=status.HTTP_200_OK)


class TeamsView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def post(self, request, format=None):
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
                tokens=[self.request.auth],
            )
        )

        return Response(status=status.HTTP_201_CREATED)


class CheckTeamNameView(APIView):
    def post(self, request, format=None):
        serializer = serializers.TeamNameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        name = serializer.data["name"]
        response = {}
        if Team.objects.filter(name=name).exists():
            response["exist"] = True
        else:
            response["exist"] = False

        return Response(response, status=status.HTTP_200_OK)


class ConfirmEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        confirm = ConfirmEmail.objects.get(user=self.request.user)
        serializer = serializers.AvailableTriesSerializer(confirm)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = serializers.ConfirmEmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        code = serializer.data["code"]
        response = {}
        confirm_email = ConfirmEmail.objects.get(
            user=self.request.user,
        )

        expiry = confirm_email.expiry
        timedelta = datetime.timedelta(
            hours=expiry.hour,
            minutes=expiry.minute,
            seconds=expiry.second,
        )

        if timezone.now() <= (self.request.user.date_joined + timedelta):
            if confirm_email.code == code:
                response["confirmed"] = True
                confirm_email.confirmed = True
            else:
                response["confirmed"] = False
                confirm_email.available_tries -= 1
                response["available_tries"] = confirm_email.available_tries
            confirm_email.save()

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class JoinTeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def put(self, request, format=None):
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
                text=f'Пользователь "{self.request.user.username}" хочет присоединиться к вашей команде!',
                image=self.request.user.profile.image.url,
                time=timestamp,
                tokens=[token.key],
            )
        )

        return Response(status=status.HTTP_200_OK)


class AcceptIntoTeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def put(self, request, format=None):
        try:
            team = Team.objects.get(admin=self.request.user)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.UsernameSerializer(data=self.request.data)
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
                text=f'Пользователь "{self.request.user.username}" хочет присоединиться к вашей команде!',
                image=self.request.user.profile.image.url,
                time=timestamp,
                tokens=[token.key],
            )
        )

        return Response(status=status.HTTP_200_OK)


class GroupView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, AdminTeamPermission]

    def put(self, request, format=None):
        serializer = serializers.GroupPutSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        supervisor_user = serializer.validated_data["supervisor_user"]
        subordinate_user = serializer.validated_data["subordinate_user"]

        if not (
            supervisor_user.profile.team == self.request.team
            and subordinate_user.profile.team == self.request.team
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if (self.request.user == supervisor_user) and (
            self.request.user == subordinate_user
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            supervisor_user_subordinates = supervisor_user.profile.get_subordinates()
            subordinate_user_subordinates = subordinate_user.profile.get_subordinates()
            if subordinate_user in supervisor_user_subordinates:
                return Response(status=status.HTTP_200_OK)
            elif supervisor_user in subordinate_user_subordinates:
                supervisor_supervisor = subordinate_user.profile.supervisor
                subordinate_user.profile.supervisor = supervisor_user
                supervisor_user.profile.supervisor = supervisor_supervisor
            else:
                subordinate_user.profile.supervisor = supervisor_user
                subordinate_user.profile.save()
            subordinate_user.profile.save()
            supervisor_user.profile.save()
            return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        serializer = serializers.GroupDeleteSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.profile.supervisor = None
        user.profile.save()

        return Response(status=status.HTTP_200_OK)


class UserTeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, AdminTeamPermission]

    def get(self, request, username, format=None):
        try:
            user = User.objects.get(
                Q(username__icontains=username) | Q(username__iexact=username)
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UsernameSerializer(user.username)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, username, format=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_200_OK)


class SuggestEmployeeView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, AdminTeamPermission]

    def post(self, request, format=None):
        serializer = serializers.UsernameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        try:
            user = User.objects.filter(
                Q(profile__team=request.team)
                & (Q(username__icontains=username) | Q(username__iexact=username))
            ).first()
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_serializer = serializers.UserWithImageSerializer(user.profile)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class SuggestTeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def post(self, request, format=None):
        serializer = serializers.TeamNameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data["name"]
        try:
            team = Team.objects.filter(
                Q(name__icontains=name) | Q(name__iexact=name)
            ).first()
        except Team.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        team_serializer = serializers.TeamSerializer(team)
        return Response(team_serializer.data, status=status.HTTP_200_OK)


class LeaveTeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, TeamPermission]

    def put(self, request, format=None):
        self.request.user.profile.team = None
        self.request.user.profile.save()
        return Response(status=status.HTTP_200_OK)
'''