import datetime
import json
from typing import Any
from unittest.mock import Mock, patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password  # type: ignore
from django.core.files.uploadedfile import SimpleUploadedFile
from google.protobuf.timestamp_pb2 import Timestamp  # type: ignore
from rest_framework.authtoken.models import Token

from account.constants import (
    DEFAULT_PROFILE_DESCRIPTION,
    DEFAULT_PROFILE_JOB_TITLE,
    EXPIRY_TIME,
    MAX_AVAILABLE_TRIES,
    PREFIX_HOST,
    TEST_PREFIX_HOST,
)
from account.pb.notifications_pb2 import NotificationRequest
from account.pb.tasks_pb2 import UserRequest
from tests.helpers import check_model_fields
from tests.unit_tests.base import UnitTest
from users.models import ConfirmEmail, Profile, Team

User = get_user_model()
user_data: dict[str, Any] = {
    "first_name": "first name",
    "last_name": "last name",
    "email": "email@email.com",
    "username": "username",
    "password": "password",
}


class TestLoginView(UnitTest):
    def test_post(self) -> None:
        User.objects.create_user(**user_data)

        response = self.client.post(
            TEST_PREFIX_HOST + "login/",
            data=json.dumps(
                {
                    "username": user_data["username"],
                    "password": user_data["password"],
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["token"])


class TestRegisterView(UnitTest):
    @patch("users.views.Timestamp.GetCurrentTime")
    @patch("users.views.Timestamp.__init__", return_value=None)
    @patch("users.views.notifications_client.Notify")
    @patch("users.views.tasks_client.AddUser")
    @patch("users.views.send_mail")
    def test_post(
        self,
        mock_send_mail: Mock,
        mock_tasks_client_AddUser: Mock,
        mock_notifications_client_Notify: Mock,
        mock_timestamp__init__: Mock,
        mock_timestamp_GetCurrentTime: Mock,
    ) -> None:
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        mock_timestamp_GetCurrentTime.return_value = timestamp

        response = self.client.post(
            TEST_PREFIX_HOST + "register/",
            data=json.dumps(user_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data["token"])

        confirm_email = ConfirmEmail.objects.all()[0]
        user_model = User.objects.all()[0]
        profile = Profile.objects.all()[0]

        self.assertRegex(str(confirm_email.code), "^[0-9]{6}$")
        self.assertEqual(confirm_email.expiry, EXPIRY_TIME)
        self.assertEqual(confirm_email.available_tries, MAX_AVAILABLE_TRIES)
        self.assertEqual(confirm_email.user_id, user_model.id)

        self.assertEqual(profile.job_title, DEFAULT_PROFILE_JOB_TITLE)
        self.assertEqual(profile.description, DEFAULT_PROFILE_DESCRIPTION)
        self.assertEqual(profile.user_id, user_model.id)

        mock_tasks_client_AddUser.assert_called_once_with(
            UserRequest(
                id=str(user_model.id),
                image=user_model.profile.image.url,
                username=user_model.username,
            )
        )

        mock_notifications_client_Notify.assert_called_once_with(
            NotificationRequest(
                text="Вы успешно зарегистрировались.",
                image=user_model.profile.image.url,
                time=timestamp,
                tokens=[response.data["token"]],
            )
        )

        mock_send_mail.assert_called_once_with(
            "Подтверждение email",
            f"Введите этот код: {confirm_email.code}",
            settings.EMAIL_HOST_USER,
            [user_model.email],
        )

        check_model_fields(
            self,
            user_model,
            user_data,
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
        )


class TestChangeUsernameView(UnitTest):
    @patch("users.views.Timestamp.GetCurrentTime")
    @patch("users.views.Timestamp.__init__", return_value=None)
    @patch("users.views.notifications_client.Notify")
    @patch("users.views.tasks_client.ChangeUser")
    def test_put(
        self,
        mock_tasks_client_ChangeUser: Mock,
        mock_notifications_client_Notify: Mock,
        mock_timestamp__init__: Mock,
        mock_timestamp_GetCurrentTime: Mock,
    ) -> None:
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        mock_timestamp_GetCurrentTime.return_value = timestamp

        user = User.objects.create_user(**user_data)

        ConfirmEmail.objects.create(
            code="111111",
            user=user,
            confirmed=True,
        )

        Profile.objects.create(
            user=user,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            TEST_PREFIX_HOST + "change_username/",
            data=json.dumps(
                {
                    "username": "username1",
                }
            ),
            content_type="application/json",
        )

        updated_user = User.objects.all()[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_user.username, "username1")

        mock_tasks_client_ChangeUser.assert_called_once_with(
            UserRequest(
                id=str(updated_user.id),
                image=updated_user.profile.image.url,
                username=updated_user.username,
            )
        )

        mock_notifications_client_Notify.assert_called_once_with(
            NotificationRequest(
                text="Имя пользователя было успешно изменено.",
                image=updated_user.profile.image.url,
                time=timestamp,
                tokens=[token.key],
            )
        )


class TestChangePasswordView(UnitTest):
    @patch("users.views.Timestamp.GetCurrentTime")
    @patch("users.views.Timestamp.__init__", return_value=None)
    @patch("users.views.notifications_client.Notify")
    def test_put(
        self,
        mock_notifications_client_Notify: Mock,
        mock_timestamp__init__: Mock,
        mock_timestamp_GetCurrentTime: Mock,
    ) -> None:
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        mock_timestamp_GetCurrentTime.return_value = timestamp

        user = User.objects.create_user(**user_data)

        ConfirmEmail.objects.create(
            code="111111",
            user=user,
            confirmed=True,
        )

        Profile.objects.create(
            user=user,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            TEST_PREFIX_HOST + "change_password/",
            data=json.dumps(
                {
                    "password": "Password111",
                    "repeated_password": "Password111",
                }
            ),
            content_type="application/json",
        )

        updated_user = User.objects.all()[0]
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            check_password(
                "Password111",
                updated_user.password,
            )
        )

        mock_notifications_client_Notify.assert_called_once_with(
            NotificationRequest(
                text="Пароль был успешно изменен.",
                image=updated_user.profile.image.url,
                time=timestamp,
                tokens=[token.key],
            )
        )


class TestCheckUsernameView(UnitTest):
    def test_post(self) -> None:
        User.objects.create_user(**user_data)

        first_response = self.client.post(
            TEST_PREFIX_HOST + "check_username/",
            data=json.dumps({"username": "username"}),
            content_type="application/json",
        )

        second_response = self.client.post(
            TEST_PREFIX_HOST + "check_username/",
            data=json.dumps({"username": "username1"}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)

        self.assertTrue(first_response.data["exist"])
        self.assertEqual(first_response.data["available"], "username1")
        self.assertFalse(second_response.data["exist"])


class TestCheckEmailView(UnitTest):
    def test_post(self) -> None:
        User.objects.create_user(**user_data)

        first_response = self.client.post(
            TEST_PREFIX_HOST + "check_email/",
            data=json.dumps({"email": "email@email.com"}),
            content_type="application/json",
        )

        second_response = self.client.post(
            TEST_PREFIX_HOST + "check_email/",
            data=json.dumps({"email": "new@email.email"}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)

        self.assertTrue(first_response.data["exist"])
        self.assertFalse(second_response.data["exist"])


class TestAuthorization(UnitTest):
    def test_get(self) -> None:
        user = User.objects.create_user(**user_data)
        token = Token.objects.create(user=user)

        unauthorized_response = self.client.get(TEST_PREFIX_HOST + "authorization/")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        authorized_response = self.client.get(TEST_PREFIX_HOST + "authorization/")

        self.assertEqual(unauthorized_response.status_code, 401)
        self.assertEqual(authorized_response.status_code, 200)


class TestAuthorizationWithEmail(UnitTest):
    def test_get(self) -> None:
        user = User.objects.create_user(**user_data)
        token = Token.objects.create(user=user)

        confirm_email = ConfirmEmail.objects.create(
            code="111111",
            user=user,
            confirmed=False,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        unauthorized_response = self.client.get(
            TEST_PREFIX_HOST + "authorization_with_email/"
        )

        confirm_email.confirmed = True
        confirm_email.save()

        authorized_response = self.client.get(
            TEST_PREFIX_HOST + "authorization_with_email/"
        )

        self.assertEqual(unauthorized_response.status_code, 403)
        self.assertEqual(authorized_response.status_code, 200)


class TestConfirmEmailView(UnitTest):
    def test_get(self) -> None:
        user = User.objects.create_user(**user_data)
        ConfirmEmail.objects.create(
            code="123456",
            user=user,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(TEST_PREFIX_HOST + "confirm_email/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["available_tries"], 3)

    def test_post_if_code_is_right(self):
        user = User.objects.create_user(**user_data)

        ConfirmEmail.objects.create(
            code="123456",
            user=user,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(
            TEST_PREFIX_HOST + "confirm_email/",
            data=json.dumps({"code": "123456"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["confirmed"])

    def test_post_if_code_is_wrong(self) -> None:
        user = User.objects.create_user(**user_data)

        ConfirmEmail.objects.create(
            code="123456",
            user=user,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(
            TEST_PREFIX_HOST + "confirm_email/",
            data=json.dumps({"code": "123457"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.data["confirmed"])
        self.assertEqual(response.data["available_tries"], 2)

    def test_post_if_expiry(self) -> None:
        changed_user_data = user_data.copy()
        changed_user_data["date_joined"] = datetime.datetime(1970, 1, 1)
        user = User.objects.create_user(**changed_user_data)

        ConfirmEmail.objects.create(
            code="123456",
            user=user,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(
            TEST_PREFIX_HOST + "confirm_email/",
            data=json.dumps({"code": "123456"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)


class TestSettingsView(UnitTest):
    def test_get(self) -> None:
        user = User.objects.create_user(**user_data)

        Profile.objects.create(
            user=user,
            job_title="Должность",
            description="Описание отсутствует.",
        )

        ConfirmEmail.objects.create(
            code="123456",
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.get(TEST_PREFIX_HOST + "settings/")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["job_title"], "Должность")
        self.assertEqual(response.data["description"], "Описание отсутствует.")
        self.assertEqual(response.data["user"]["first_name"], "first name")
        self.assertEqual(response.data["user"]["last_name"], "last name")

    @patch("users.views.tasks_client.ChangeUser")
    def test_put(
        self,
        mock_tasks_client_ChangeUser: Mock,
    ) -> None:
        user = User.objects.create_user(**user_data)
        Profile.objects.create(user=user)

        ConfirmEmail.objects.create(
            code="123456",
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        changed_data = {
            "job_title": "Должность",
            "description": "Новое описание.",
            "first_name": "Иван",
            "last_name": "Иванов",
            "image": SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        }

        response = self.client.put(
            TEST_PREFIX_HOST + "settings/",
            data=changed_data,
        )

        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.all()[0]
        profile_model = Profile.objects.all()[0]

        self.assertEqual(updated_user.first_name, changed_data["first_name"])
        self.assertEqual(updated_user.last_name, changed_data["last_name"])

        self.assertEqual(profile_model.job_title, changed_data["job_title"])
        self.assertEqual(profile_model.description, changed_data["description"])

        mock_tasks_client_ChangeUser.assert_called_once_with(
            UserRequest(
                id=str(updated_user.id),
                image=updated_user.profile.image.url,
                username=updated_user.username,
            )
        )

    @patch("users.views.tasks_client.DeleteUser")
    def test_delete(
        self,
        mock_tasks_client_DeleteUser: Mock,
    ) -> None:
        user = User.objects.create_user(**user_data)
        Profile.objects.create(user=user)

        ConfirmEmail.objects.create(
            code="123456",
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.delete(TEST_PREFIX_HOST + "settings/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), 0)

        mock_tasks_client_DeleteUser.assert_called_once_with(
            UserRequest(id=str(user.id))
        )


class TestAvatarView(UnitTest):
    def test_get(self) -> None:
        user = User.objects.create_user(**user_data)
        Profile.objects.create(user=user)

        ConfirmEmail.objects.create(
            code="123456",
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.get(TEST_PREFIX_HOST + "avatar/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["image"], "/images/default.png")


class TestGroupView(UnitTest):
    def test_put_third_case(self) -> None:
        admin = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="admin",
            password="password",
        )

        supervisor_user = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="username1",
            password="password",
        )

        subordinate_user = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="username2",
            password="password",
        )

        Profile.objects.create(user=admin)

        ConfirmEmail.objects.create(
            code="123456",
            user=admin,
            confirmed=True,
        )

        team = Team.objects.create(
            name="name",
            description="Описание команды",
            admin=admin,
        )

        admin.profile.team = team
        admin.profile.save()

        Profile.objects.create(
            user=supervisor_user,
            team=team,
        )

        Profile.objects.create(
            user=subordinate_user,
            team=team,
        )

        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            TEST_PREFIX_HOST + "group/",
            data=json.dumps(
                {
                    "supervisor_username": "username1",
                    "subordinate_username": "username2",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        supervisor_profile = Profile.objects.get(user=supervisor_user)
        subordinate_profile = Profile.objects.get(user=subordinate_user)

        self.assertIsNone(supervisor_profile.supervisor_id)
        self.assertEqual(subordinate_profile.supervisor_id, supervisor_user.id)

    def test_put_second_case(self) -> None:
        admin = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="admin",
            password="password",
        )

        supervisor_user = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="username1",
            password="password",
        )

        subordinate_user = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="username2",
            password="password",
        )

        supervisor_supervisor_user = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="username3",
            password="password",
        )

        Profile.objects.create(user=admin)

        ConfirmEmail.objects.create(
            code="123456",
            user=admin,
            confirmed=True,
        )

        team = Team.objects.create(
            name="name",
            description="Описание команды",
            admin=admin,
        )

        admin.profile.team = team
        admin.profile.save()

        Profile.objects.create(
            user=supervisor_user,
            supervisor=subordinate_user,
            team=team,
        )

        Profile.objects.create(
            user=subordinate_user,
            supervisor=supervisor_supervisor_user,
            team=team,
        )

        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            TEST_PREFIX_HOST + "group/",
            data=json.dumps(
                {
                    "supervisor_username": "username1",
                    "subordinate_username": "username2",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        supervisor_profile = Profile.objects.get(user=supervisor_user)
        subordinate_profile = Profile.objects.get(user=subordinate_user)

        self.assertEqual(
            supervisor_profile.supervisor_id, supervisor_supervisor_user.id
        )
        self.assertEqual(subordinate_profile.supervisor_id, supervisor_user.id)

    def test_put_first_case(self) -> None:
        admin = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="admin",
            password="password",
        )

        supervisor_user = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="username1",
            password="password",
        )

        subordinate_user = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="username2",
            password="password",
        )

        Profile.objects.create(user=admin)

        ConfirmEmail.objects.create(
            code="123456",
            user=admin,
            confirmed=True,
        )

        team = Team.objects.create(
            name="name",
            description="Описание команды",
            admin=admin,
        )

        admin.profile.team = team
        admin.profile.save()

        Profile.objects.create(
            user=supervisor_user,
            team=team,
        )

        Profile.objects.create(
            user=subordinate_user,
            supervisor=supervisor_user,
            team=team,
        )

        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            TEST_PREFIX_HOST + "group/",
            data=json.dumps(
                {
                    "supervisor_username": "username1",
                    "subordinate_username": "username2",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        supervisor_profile = Profile.objects.get(user=supervisor_user)
        subordinate_profile = Profile.objects.get(user=subordinate_user)

        self.assertIsNone(supervisor_profile.supervisor_id)
        self.assertEqual(subordinate_profile.supervisor_id, supervisor_user.id)

    def test_delete(self) -> None:
        admin = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="admin",
            password="password",
        )

        supervisor_user = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="username1",
            password="password",
        )

        user = User.objects.create_user(
            first_name="first name",
            last_name="last name",
            email="email@email.com",
            username="username",
            password="password",
        )

        Profile.objects.create(user=admin)

        ConfirmEmail.objects.create(
            code="123456",
            user=admin,
            confirmed=True,
        )

        team = Team.objects.create(
            name="name",
            description="Описание команды",
            admin=admin,
        )

        admin.profile.team = team
        admin.profile.save()

        Profile.objects.create(
            user=user,
            supervisor=supervisor_user,
            team=team,
        )

        Profile.objects.create(
            user=supervisor_user,
            team=team,
        )

        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.delete(
            TEST_PREFIX_HOST + "group/",
            data=json.dumps({"username": "username"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.get(user=user)
        self.assertIsNone(profile.supervisor_id)


class TestSuggestEmployeeView(UnitTest):
    def test_post_if_admin(self) -> None:
        admin = User.objects.create_user(**user_data)

        changed_user_data = user_data.copy()
        changed_user_data["email"] = "email1@email.com"
        changed_user_data["username"] = "username1"

        teammate = User.objects.create_user(**changed_user_data)

        for user in [admin, teammate]:
            Profile.objects.create(user=user)
            ConfirmEmail.objects.create(
                code="123456",
                user=user,
                confirmed=True,
            )

        team = Team.objects.create(
            name="Название",
            description="Описание.",
            admin=admin,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        admin.profile.team = team
        admin.profile.save()
        teammate.profile.team = team
        teammate.profile.save()

        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        first_response = self.client.post(
            TEST_PREFIX_HOST + "suggest_employee/",
            data=json.dumps({"username": teammate.username}),
            content_type="application/json",
        )

        second_response = self.client.post(
            TEST_PREFIX_HOST + "suggest_employee/",
            data=json.dumps({"username": teammate.username[:3]}),
            content_type="application/json",
        )

        third_response = self.client.post(
            TEST_PREFIX_HOST + "suggest_employee/",
            data=json.dumps({"username": "Wrong name"}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(third_response.status_code, 400)

        self.assertEqual(first_response.data["user"]["first_name"], teammate.first_name)
        self.assertEqual(first_response.data["user"]["last_name"], teammate.last_name)
        self.assertEqual(first_response.data["user"]["username"], teammate.username)

        self.assertEqual(
            second_response.data["user"]["first_name"], teammate.first_name
        )
        self.assertEqual(second_response.data["user"]["last_name"], teammate.last_name)
        self.assertEqual(second_response.data["user"]["username"], "username")

    def test_post_if_not_admin(self) -> None:
        admin = User.objects.create_user(**user_data)

        first_changed_user_data = user_data.copy()
        first_changed_user_data["email"] = "email1@email.com"
        first_changed_user_data["username"] = "username1"

        teammate = User.objects.create_user(**first_changed_user_data)

        second_changed_user_data = user_data.copy()
        second_changed_user_data["email"] = "email1@email.com"
        second_changed_user_data["username"] = "username2"

        supervisor = User.objects.create_user(**second_changed_user_data)

        for user in [admin, teammate, supervisor]:
            Profile.objects.create(user=user)
            ConfirmEmail.objects.create(
                code="123456",
                user=user,
                confirmed=True,
            )

        team = Team.objects.create(
            name="Название",
            description="Описание.",
            admin=admin,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        for user in [admin, teammate, supervisor]:
            user.profile.team = team
            user.profile.save()

        teammate.profile.supervisor = supervisor
        teammate.profile.save()

        token = Token.objects.create(user=supervisor)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        first_response = self.client.post(
            TEST_PREFIX_HOST + "suggest_employee/",
            data=json.dumps({"username": teammate.username}),
            content_type="application/json",
        )

        second_response = self.client.post(
            TEST_PREFIX_HOST + "suggest_employee/",
            data=json.dumps({"username": teammate.username[:3]}),
            content_type="application/json",
        )

        third_response = self.client.post(
            TEST_PREFIX_HOST + "suggest_employee/",
            data=json.dumps({"username": "Wrong name"}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(third_response.status_code, 400)

        self.assertEqual(first_response.data["user"]["first_name"], teammate.first_name)
        self.assertEqual(first_response.data["user"]["last_name"], teammate.last_name)
        self.assertEqual(first_response.data["user"]["username"], teammate.username)

        self.assertEqual(
            second_response.data["user"]["first_name"], teammate.first_name
        )
        self.assertEqual(second_response.data["user"]["last_name"], teammate.last_name)
        self.assertEqual(second_response.data["user"]["username"], "username")
