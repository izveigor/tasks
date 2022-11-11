from .base import UnitTest
from django.contrib.auth.models import User
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
)
import datetime
from unittest.mock import patch, Mock
from users.pb.users_pb2 import UserRequest


class TestLoginView(UnitTest):
    def test_post(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }
        User.objects.create_user(**user_data)

        response = self.client.post(
            "/login/",
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
    @patch("users.views.users_client.AddUser")
    @patch("users.views.send_mail")
    def test_post(
        self,
        mock_send_mail: Mock,
        mock_users_client_AddUser_mock: Mock,
    ):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        response = self.client.post(
            "/register/",
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
        self.assertEqual(confirm_email.user_id, 1)

        self.assertEqual(profile.job_title, DEFAULT_PROFILE_JOB_TITLE)
        self.assertEqual(profile.description, DEFAULT_PROFILE_DESCRIPTION)
        self.assertEqual(profile.user_id, 1)

        mock_users_client_AddUser_mock.assert_called_once_with(
            UserRequest(id=user_model.id, username=user_model.username)
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
    @patch("users.views.users_client.ChangeUser")
    def test_put(
        self,
        users_client_ChangeUser_mock: Mock,
    ):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(**user_data)

        ConfirmEmail.objects.create(
            code="111111",
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            "/change_username/",
            data=json.dumps(
                {
                    "username": "username1",
                }
            ),
            content_type="application/json",
        )

        updated_user = User.objects.all()[0]
        users_client_ChangeUser_mock.assert_called_once_with(
            UserRequest(id=updated_user.id, username=updated_user.username)
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(updated_user.username, "username1")


class TestChangePasswordView(UnitTest):
    def test_put(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }

        user = User.objects.create_user(**user_data)

        ConfirmEmail.objects.create(
            code="111111",
            user=user,
            confirmed=True,
        )

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            "/change_password/",
            data=json.dumps(
                {
                    "password": "Password111",
                    "repeated_password": "Password111",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 204)
        self.assertTrue(
            check_password(
                "Password111",
                User.objects.all()[0].password,
            )
        )


class TestCheckEmailView(UnitTest):
    def test_post(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }
        User.objects.create_user(**user_data)

        first_response = self.client.post(
            "/check_email/",
            data=json.dumps({"email": "email@email.com"}),
            content_type="application/json",
        )

        second_response = self.client.post(
            "/check_email/",
            data=json.dumps({"email": "new@email.email"}),
            content_type="application/json",
        )

        self.assertTrue(first_response.data["exist"])
        self.assertFalse(second_response.data["exist"])


class TestCheckUsernameView(UnitTest):
    def test_post(self):
        user_data = {
            "first_name": "first name",
            "last_name": "last name",
            "email": "email@email.com",
            "username": "username",
            "password": "password",
        }
        User.objects.create_user(**user_data)

        first_response = self.client.post(
            "/check_username/",
            data=json.dumps(
                {
                    "username": "username",
                }
            ),
            content_type="application/json",
        )

        second_response = self.client.post(
            "/check_username/",
            data=json.dumps(
                {
                    "username": "username1",
                }
            ),
            content_type="application/json",
        )

        self.assertTrue(first_response.data["exist"])
        self.assertEqual(first_response.data["available"], "username2")
        self.assertFalse(second_response.data["exist"])


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
