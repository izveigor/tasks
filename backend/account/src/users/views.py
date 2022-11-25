from users.methods import suggest_username
from .models import ConfirmEmail, Profile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from . import serializers
from rest_framework.authtoken.models import Token
from .methods import suggest_username
import datetime
from django.utils import timezone
import random
from django.core.mail import send_mail
from django.conf import settings
from account.permissions import EmailPermission
from account.notifications_client import notifications_client
from account.pb.notifications_pb2 import NotificationRequest
from google.protobuf.timestamp_pb2 import Timestamp
from rest_framework.authtoken.models import Token
from account.tasks_client import tasks_client
from account.pb.tasks_pb2 import UserRequest
from django.contrib.auth import get_user_model
from account.permissions import AdminTeamPermission, CreatorTeamPermission
from django.db.models import Q

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


class CheckEmailView(APIView):
    def post(self, request, format=None):
        serializer = serializers.EmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        email = serializer.data["email"]
        response = {}
        if User.objects.filter(email=email).exists():
            response["exist"] = True
        else:
            response["exist"] = False

        return Response(response, status=status.HTTP_200_OK)


class Authorization(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class AuthorizationWithEmail(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class ConfirmEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        confirm = ConfirmEmail.objects.get(user=self.request.user)
        serializer = serializers.EmailAvailableTriesSerializer(confirm)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = serializers.EmailCodeSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        code = serializer.data["code"]
        response = {}
        confirm_email = ConfirmEmail.objects.get(user=self.request.user)

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

        tasks_client.ChangeUser(
            UserRequest(
                id=str(self.request.user.id),
                image=self.request.user.profile.image.url,
                username=self.request.user.username,
            )
        )

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        user = self.request.user
        user_id = str(user.id)
        user.delete()

        tasks_client.DeleteUser(UserRequest(id=user_id))
        return Response(status=status.HTTP_200_OK)


class AvatarView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def get(self, request, format=None):
        serializer = serializers.AvatarSerializer(self.request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class SuggestEmployeeView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, CreatorTeamPermission]

    def post(self, request, format=None):
        serializer = serializers.UsernameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        if request.team.admin == self.request.team.admin:
            user = User.objects.filter(
                Q(profile__team=request.team)
                & Q(username__icontains=username)
            ).first()
        else:
            user = User.objects.filter(
                Q(profile__team=request.team)
                & Q(username__icontains=username)
                & Q(profile__supervisor=self.request.user)
            ).first()

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_serializer = serializers.UserWithImageSerializer(user.profile)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


'''
class UserView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission]

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class LeaveTeamView(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, TeamPermission]

    def put(self, request, format=None):
        self.request.user.profile.team = None
        self.request.user.profile.save()
        return Response(status=status.HTTP_200_OK)
'''