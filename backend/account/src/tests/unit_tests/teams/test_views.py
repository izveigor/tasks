from tests.unit_tests.base import UnitTest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from users.models import ConfirmEmail, Profile
from teams.models import Team
from account.constants import TEST_PREFIX_HOST
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import json
from unittest.mock import patch, Mock
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


class TestAuthorizationLikeTeammate(UnitTest):
    def test_get(self):
        admin = User.objects.create_user(**user_data)

        changed_user_data = user_data.copy()
        changed_user_data["email"] = "email1@email.com"
        changed_user_data["username"] = "username1"

        user = User.objects.create_user(**changed_user_data)
        token = Token.objects.create(user=user)

        for u in [user, admin]:
            ConfirmEmail.objects.create(
                code="111111",
                user=u,
                confirmed=True,
            )

            Profile.objects.create(
                user=u,
                image=SimpleUploadedFile(
                    name="default.png",
                    content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                    content_type="image/png",
                ),
            )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        unauthorized_response = self.client.get(TEST_PREFIX_HOST+"authorization_like_teammate/")

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

        user.profile.team = team
        user.profile.save()

        authorized_response = self.client.get(TEST_PREFIX_HOST+"authorization_like_teammate/")

        self.assertEqual(unauthorized_response.status_code, 403)
        self.assertEqual(authorized_response.status_code, 200)


class TestAuthorizationLikeAdmin(UnitTest):
    def test_get(self):
        admin = User.objects.create_user(**user_data)
        token = Token.objects.create(user=admin)

        ConfirmEmail.objects.create(
            code="111111",
            user=admin,
            confirmed=True,
        )

        Profile.objects.create(
            user=admin,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        unauthorized_response = self.client.get(TEST_PREFIX_HOST+"authorization_like_admin/")

        Team.objects.create(
            name="Название",
            description="Описание.",
            admin=admin,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        authorized_response = self.client.get(TEST_PREFIX_HOST+"authorization_like_admin/")

        self.assertEqual(unauthorized_response.status_code, 403)
        self.assertEqual(authorized_response.status_code, 200)


class TestAuthorizationLikeCreator(UnitTest):
    def test_get(self):
        user = User.objects.create_user(**user_data)

        changed_user_data = user_data.copy()
        changed_user_data["email"] = "email1@email.com"
        changed_user_data["username"] = "username2"

        supervisor = User.objects.create_user(**changed_user_data)
        token = Token.objects.create(user=supervisor)

        ConfirmEmail.objects.create(
            code="111111",
            user=supervisor,
            confirmed=True,
        )

        user_profile = Profile.objects.create(
            user=user,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        Profile.objects.create(
            user=supervisor,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        unauthorized_response = self.client.get(TEST_PREFIX_HOST+"authorization_like_creator/")

        user_profile.supervisor = supervisor
        user_profile.save()

        authorized_response = self.client.get(TEST_PREFIX_HOST+"authorization_like_creator/")

        self.assertEqual(unauthorized_response.status_code, 403)
        self.assertEqual(authorized_response.status_code, 200)


class TestCheckTeamNameView(UnitTest):
    def test_post(self):
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
            TEST_PREFIX_HOST+"check_team_name/",
            data=json.dumps({"name": "name"}),
            content_type="application/json",
        )

        second_response = self.client.post(
            TEST_PREFIX_HOST+"check_team_name/",
            data=json.dumps({"name": "name1"}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)

        self.assertTrue(first_response.data["exist"])
        self.assertFalse(second_response.data["exist"])


class TestTeamView(UnitTest):
    def test_get(self):
        user = User.objects.create_user(**user_data)

        ConfirmEmail.objects.create(
            code="123456",
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
            TEST_PREFIX_HOST+"team/",
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["name"], "Название")
        self.assertEqual(response.data["description"], "Описание.")

    def test_put(self):
        user = User.objects.create_user(**user_data)

        ConfirmEmail.objects.create(
            code="123456",
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
            TEST_PREFIX_HOST+"team/",
            data={
                "name": "Новое название",
                "description": "Описание.",
                "image": SimpleUploadedFile(
                    name="default.png",
                    content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                    content_type="image/png",
                ),
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        admin = User.objects.create_user(**user_data)

        first_changed_user_data = user_data.copy()
        first_changed_user_data["email"] = "email1@email.com"
        first_changed_user_data["username"] = "username1"

        second_changed_user_data = user_data.copy()
        second_changed_user_data["email"] = "email2@email.com"
        second_changed_user_data["username"] = "username2"

        first_user = User.objects.create_user(**first_changed_user_data)
        second_user = User.objects.create_user(**second_changed_user_data)

        for user in [admin, first_user, second_user]:
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

        for user in [first_user, second_user]:
            user.profile.team = team
            user.profile.save()

        first_user.profile.supervisor = second_user
        first_user.profile.save()

        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.delete(TEST_PREFIX_HOST+"team/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Team.objects.all()), 0)
        self.assertIsNone(Profile.objects.get(user__username="username1").supervisor)


class TestJoinTeamView(UnitTest):
    @patch("users.views.Timestamp.GetCurrentTime")
    @patch("users.views.Timestamp.__init__", return_value=None)
    @patch("teams.views.notifications_client.Notify")
    def test_put(
        self,
        mock_notifications_client_Notify: Mock,
        mock_timestamp__init__: Mock,
        mock_timestamp_GetCurrentTime: Mock,
    ):
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        mock_timestamp_GetCurrentTime.return_value = timestamp

        admin = User.objects.create(**user_data)
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

        changed_user_data = user_data.copy()
        changed_user_data["email"] = "email1@email.com"
        changed_user_data["username"] = "username1"

        user = User.objects.create(**changed_user_data)
        ConfirmEmail.objects.create(
            code="123456",
            user=user,
            confirmed=True,
        )

        user_token = Token.objects.create(user=user)
        Profile.objects.create(user=user)
        admin_token = Token.objects.create(user=admin)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = self.client.put(
            TEST_PREFIX_HOST+"join/",
            data=json.dumps({"name": team.name}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        mock_notifications_client_Notify.assert_called_once_with(
            NotificationRequest(
                text=f'Пользователь "{user.username}" хочет присоединиться к вашей команде.',
                image=user.profile.image.url,
                time=timestamp,
                tokens=[admin_token.key],
            )
        )


class TestAcceptIntoTeamView(UnitTest):
    @patch("users.views.Timestamp.GetCurrentTime")
    @patch("users.views.Timestamp.__init__", return_value=None)
    @patch("teams.views.notifications_client.Notify")
    def test_put(
        self,
        mock_notifications_client_Notify: Mock,
        mock_timestamp__init__: Mock,
        mock_timestamp_GetCurrentTime: Mock,
    ):
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        mock_timestamp_GetCurrentTime.return_value = timestamp

        admin = User.objects.create_user(**user_data)

        changed_user_data = user_data.copy()
        changed_user_data["email"] = "email1@email.com"
        changed_user_data["username"] = "username1"

        joined_user = User.objects.create_user(**changed_user_data)

        admin_token = Token.objects.create(user=admin)
        user_token = Token.objects.create(user=joined_user)

        for user in [admin, joined_user]:
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

        self.client.credentials(HTTP_AUTHORIZATION="Token " + admin_token.key)
        response = self.client.put(
            TEST_PREFIX_HOST+"accept/",
            data=json.dumps({"username": joined_user.username}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        mock_notifications_client_Notify.assert_called_once_with(
            NotificationRequest(
                text=f'Вы присоединились к команде "{team.name}".',
                image=team.image.url,
                time=timestamp,
                tokens=[user_token.key],
            )
        )
