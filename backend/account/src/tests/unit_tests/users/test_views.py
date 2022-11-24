from tests.unit_tests.base import UnitTest
import json
from tests.helpers import check_model_fields
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from users.models import Team, ConfirmEmail, Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from account.constants import (
    MAX_AVAILABLE_TRIES,
    EXPIRY_TIME,
    DEFAULT_PROFILE_DESCRIPTION,
    DEFAULT_PROFILE_JOB_TITLE,
    PREFIX_HOST,
    TEST_PREFIX_HOST,
)
import datetime
from unittest.mock import patch, Mock
from django.contrib.auth import get_user_model
from account.pb.tasks_pb2 import UserRequest
from account.pb.notifications_pb2 import NotificationRequest
from google.protobuf.timestamp_pb2 import Timestamp

User = get_user_model()
user_data = {
    "first_name": "first name",
    "last_name": "last name",
    "email": "email@email.com",
    "username": "username",
    "password": "password",
}


class TestLoginView(UnitTest):
    def test_post(self):
        User.objects.create_user(**user_data)

        response = self.client.post(
            TEST_PREFIX_HOST+"login/",
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
    ):
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        mock_timestamp_GetCurrentTime.return_value = timestamp

        response = self.client.post(
            TEST_PREFIX_HOST+"register/",
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
    ):
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
            TEST_PREFIX_HOST+"change_username/",
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
    ):
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
            TEST_PREFIX_HOST+"change_password/",
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
    def test_post(self):
        User.objects.create_user(**user_data)

        first_response = self.client.post(
            TEST_PREFIX_HOST+"check_username/",
            data=json.dumps({"username": "username"}),
            content_type="application/json",
        )

        second_response = self.client.post(
            TEST_PREFIX_HOST+"check_username/",
            data=json.dumps({"username": "username1"}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)

        self.assertTrue(first_response.data["exist"])
        self.assertEqual(first_response.data["available"], "username1")
        self.assertFalse(second_response.data["exist"])


class TestCheckEmailView(UnitTest):
    def test_post(self):
        User.objects.create_user(**user_data)

        first_response = self.client.post(
            TEST_PREFIX_HOST+"check_email/",
            data=json.dumps({"email": "email@email.com"}),
            content_type="application/json",
        )

        second_response = self.client.post(
            TEST_PREFIX_HOST+"check_email/",
            data=json.dumps({"email": "new@email.email"}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)

        self.assertTrue(first_response.data["exist"])
        self.assertFalse(second_response.data["exist"])


class TestAuthorization(UnitTest):
    def test_get(self):
        user = User.objects.create_user(**user_data)
        token = Token.objects.create(user=user)

        unauthorized_response = self.client.get(TEST_PREFIX_HOST+"authorization/")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        authorized_response = self.client.get(TEST_PREFIX_HOST+"authorization/")

        self.assertEqual(unauthorized_response.status_code, 401)
        self.assertEqual(authorized_response.status_code, 200)


class TestAuthorizationWithEmail(UnitTest):
    def test_get(self):
        user = User.objects.create_user(**user_data)
        token = Token.objects.create(user=user)

        confirm_email = ConfirmEmail.objects.create(
            code="111111",
            user=user,
            confirmed=False,
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        unauthorized_response = self.client.get(TEST_PREFIX_HOST+"authorization_with_email/")

        confirm_email.confirmed = True
        confirm_email.save()

        authorized_response = self.client.get(TEST_PREFIX_HOST+"authorization_with_email/")

        self.assertEqual(unauthorized_response.status_code, 403)
        self.assertEqual(authorized_response.status_code, 200)


'''
class TestCheckTeamNameView(UnitTest):
    def test_post(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }
        user = User.objects.create_user(**user_data)

        Team.objects.create(
            name="name",
            description="Описание команды",
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
            admin=user,
        )

        first_response = self.client.post(
            "/check_team/",
            data=json.dumps(
                {
                    "name": "name",
                }
            ),
            content_type="application/json",
        )

        second_response = self.client.post(
            "/check_team/",
            data=json.dumps(
                {
                    "name": "name1",
                }
            ),
            content_type="application/json",
        )

        self.assertTrue(first_response.data["exist"])
        self.assertFalse(second_response.data["exist"])


class TestConfirmEmailView(UnitTest):
    def test_post_if_code_is_right(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(
            **user_data,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(
            "/confirm_email/",
            data=json.dumps(
                {
                    "code": 123456,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["confirmed"])

    def test_post_if_code_is_wrong(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(
            **user_data,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(
            "/confirm_email/",
            data=json.dumps(
                {
                    "code": 123457,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.data["confirmed"])
        self.assertEqual(response.data["available_tries"], 2)

    def test_post_if_expiry(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user_data["date_joined"] = datetime.datetime(1970, 1, 1)
        user = User.objects.create_user(
            **user_data,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(
            "/confirm_email/",
            data=json.dumps(
                {
                    "code": 123456,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)


class TestTeamView(UnitTest):
    def test_get(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(
            **user_data,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
            confirmed=True,
        )

        Team.objects.create(
            name="Название",
            description="Описание.",
            admin=user,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(
            "/team/1/",
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["name"], "Название")
        self.assertEqual(response.data["description"], "Описание.")

    def test_put(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(
            **user_data,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
            confirmed=True,
        )

        Team.objects.create(
            name="Название",
            description="Описание.",
            admin=user,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            "/team/1/",
            data=json.dumps(
                {
                    "name": "Новое название",
                    "description": "Описание.",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(
            **user_data,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
            confirmed=True,
        )

        Team.objects.create(
            name="Название",
            description="Описание.",
            admin=user,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.delete(
            "/team/1/",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Team.objects.all()), 0)


class TestViews(UnitTest):
    def test_post(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(
            **user_data,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(
            "/teams/",
            data=json.dumps(
                {
                    "name": "Название",
                    "description": "Описание.",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        team = Team.objects.all()[0]

        self.assertEqual(team.name, "Название")
        self.assertEqual(team.description, "Описание.")
        self.assertEqual(team.admin, user)


class TestProfileView(UnitTest):
    def test_get(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(
            **user_data,
        )

        Profile.objects.create(
            user=user,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.get(
            "/profile/1",
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["job_title"], DEFAULT_PROFILE_JOB_TITLE)
        self.assertEqual(response.data["description"], DEFAULT_PROFILE_DESCRIPTION)

        self.assertEqual(response.data["user"]["first_name"], "first name")
        self.assertEqual(response.data["user"]["last_name"], "last name")


class TestSettingsView(UnitTest):
    def test_put(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(
            **user_data,
        )

        Profile.objects.create(
            user=user,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        changed_data = {
            "job_title": "Должность",
            "description": "Новое описание.",
            "user": {
                "first_name": "Иван",
                "last_name": "Иванов",
            },
        }

        response = self.client.put(
            "/settings/",
            data=json.dumps(changed_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        user_model = User.objects.all()[0]
        profile_model = Profile.objects.all()[0]

        self.assertEqual(user_model.first_name, changed_data["user"]["first_name"])
        self.assertEqual(user_model.last_name, changed_data["user"]["last_name"])

        self.assertEqual(profile_model.job_title, changed_data["job_title"])
        self.assertEqual(profile_model.description, changed_data["description"])

    @patch("users.views.users_client.DeleteUser")
    def test_delete(
        self,
        users_client_DeleteUser_mock: Mock,
    ):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(
            **user_data,
        )

        Profile.objects.create(
            user=user,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        changed_data = {
            "job_title": "Должность",
            "description": "Новое описание.",
            "user": {
                "first_name": "Иван",
                "last_name": "Иванов",
            },
        }

        response = self.client.delete(
            "/settings/",
            data=json.dumps(changed_data),
            content_type="application/json",
        )

        users_client_DeleteUser_mock.assert_called_once_with(
            UserRequest(
                id=user.id,
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), 0)


class TestGroupView(UnitTest):
    def test_put_third_case(self):
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

        Profile.objects.create(
            user=admin,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=admin,
            confirmed=True,
        )

        team = Team.objects.create(
            name="name",
            description="Описание команды",
            admin=admin,
        )

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
            "/group/",
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
        self.assertEqual(subordinate_profile.supervisor_id, 2)

    def test_put_second_case(self):
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

        Profile.objects.create(
            user=admin,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=admin,
            confirmed=True,
        )

        team = Team.objects.create(
            name="name",
            description="Описание команды",
            admin=admin,
        )

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
            "/group/",
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

        self.assertEqual(supervisor_profile.supervisor_id, 4)
        self.assertEqual(subordinate_profile.supervisor_id, 2)

    def test_put_first_case(self):
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

        Profile.objects.create(
            user=admin,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=admin,
            confirmed=True,
        )

        team = Team.objects.create(
            name="name",
            description="Описание команды",
            admin=admin,
        )

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
            "/group/",
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
        self.assertEqual(subordinate_profile.supervisor_id, 2)

    def test_delete(self):
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

        Profile.objects.create(
            user=admin,
        )

        ConfirmEmail.objects.create(
            code=123456,
            user=admin,
            confirmed=True,
        )

        team = Team.objects.create(
            name="name",
            description="Описание команды",
            admin=admin,
        )

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
            "/group/",
            data=json.dumps(
                {
                    "username": "username",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.get(user=user)
        self.assertIsNone(profile.supervisor_id)
'''