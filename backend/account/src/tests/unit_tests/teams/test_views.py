import json
from unittest.mock import Mock, patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from google.protobuf.timestamp_pb2 import Timestamp  # type: ignore
from rest_framework.authtoken.models import Token

from account.constants import TEST_PREFIX_HOST
from account.pb.notifications_pb2 import NotificationRequest
from teams.models import Team
from tests.unit_tests.base import UnitTest
from users.models import ConfirmEmail, Profile

User = get_user_model()
user_data = {
    "first_name": "first name",
    "last_name": "last name",
    "email": "email@email.com",
    "username": "username",
    "password": "password",
}


class TestAuthorizationLikeTeammate(UnitTest):
    def test_get(self) -> None:
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
                    content=open(
                        settings.MEDIA_ROOT + "/" + "default.png", "rb"
                    ).read(),
                    content_type="image/png",
                ),
            )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        unauthorized_response = self.client.get(
            TEST_PREFIX_HOST + "authorization_like_teammate/"
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

        user.profile.team = team
        user.profile.save()

        authorized_response = self.client.get(
            TEST_PREFIX_HOST + "authorization_like_teammate/"
        )

        self.assertEqual(unauthorized_response.status_code, 403)
        self.assertEqual(authorized_response.status_code, 200)


class TestAuthorizationLikeAdmin(UnitTest):
    def test_get(self) -> None:
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
        unauthorized_response = self.client.get(
            TEST_PREFIX_HOST + "authorization_like_admin/"
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

        authorized_response = self.client.get(
            TEST_PREFIX_HOST + "authorization_like_admin/"
        )

        self.assertEqual(unauthorized_response.status_code, 403)
        self.assertEqual(authorized_response.status_code, 200)


class TestAuthorizationLikeCreator(UnitTest):
    def test_get(self) -> None:
        admin = User.objects.create_user(**user_data)

        first_changed_user_data = user_data.copy()
        first_changed_user_data["email"] = "email1@email.com"
        first_changed_user_data["username"] = "username1"

        user = User.objects.create_user(**first_changed_user_data)

        second_changed_user_data = user_data.copy()
        second_changed_user_data["email"] = "email2@email.com"
        second_changed_user_data["username"] = "username2"

        supervisor = User.objects.create_user(**second_changed_user_data)
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

        supervisor.profile.team = team
        supervisor.profile.save()

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        unauthorized_response = self.client.get(
            TEST_PREFIX_HOST + "authorization_like_creator/"
        )

        user_profile.supervisor = supervisor
        user_profile.save()

        authorized_response = self.client.get(
            TEST_PREFIX_HOST + "authorization_like_creator/"
        )

        self.assertEqual(unauthorized_response.status_code, 403)
        self.assertEqual(authorized_response.status_code, 200)


class TestCheckTeamNameView(UnitTest):
    def test_post(self) -> None:
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
            TEST_PREFIX_HOST + "check_team_name/",
            data=json.dumps({"name": "name"}),
            content_type="application/json",
        )

        second_response = self.client.post(
            TEST_PREFIX_HOST + "check_team_name/",
            data=json.dumps({"name": "name1"}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)

        self.assertTrue(first_response.data["exist"])
        self.assertFalse(second_response.data["exist"])


class TestTeamView(UnitTest):
    def test_get(self) -> None:
        user = User.objects.create_user(**user_data)

        Profile.objects.create(user=user)
        ConfirmEmail.objects.create(
            code="123456",
            user=user,
            confirmed=True,
        )

        team = Team.objects.create(
            name="Название",
            description="Описание.",
            admin=user,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        user.profile.team = team
        user.profile.save()

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(
            TEST_PREFIX_HOST + "team/",
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["name"], "Название")
        self.assertEqual(response.data["description"], "Описание.")

    def test_put(self) -> None:
        user = User.objects.create_user(**user_data)

        Profile.objects.create(user=user)
        ConfirmEmail.objects.create(
            code="123456",
            user=user,
            confirmed=True,
        )

        team = Team.objects.create(
            name="Название",
            description="Описание.",
            admin=user,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        user.profile.team = team
        user.profile.save()

        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(
            TEST_PREFIX_HOST + "team/",
            data={
                "name": "Новое название",
                "description": "Описание.",
                "image": SimpleUploadedFile(
                    name="default.png",
                    content=open(
                        settings.MEDIA_ROOT + "/" + "default.png", "rb"
                    ).read(),
                    content_type="image/png",
                ),
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_delete(self) -> None:
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

        admin.profile.team = team
        admin.profile.save()

        for user in [first_user, second_user]:
            user.profile.team = team
            user.profile.save()

        first_user.profile.supervisor = second_user
        first_user.profile.save()

        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.delete(TEST_PREFIX_HOST + "team/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Team.objects.all()), 0)
        self.assertIsNone(Profile.objects.get(user__username="username1").supervisor)


class TestJoinTeamView(UnitTest):
    @patch("teams.views.Timestamp.GetCurrentTime")
    @patch("teams.views.Timestamp.__init__", return_value=None)
    @patch("teams.views.notifications_client.Notify")
    def test_put(
        self,
        mock_notifications_client_Notify: Mock,
        mock_timestamp__init__: Mock,
        mock_timestamp_GetCurrentTime: Mock,
    ) -> None:
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
            TEST_PREFIX_HOST + "join/",
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
    ) -> None:
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
            TEST_PREFIX_HOST + "accept/",
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


class TestSuggestTeamView(UnitTest):
    def test_post(self) -> None:
        admin = User.objects.create_user(**user_data)
        Profile.objects.create(user=admin)
        ConfirmEmail.objects.create(
            code="123456",
            user=admin,
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

        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        first_response = self.client.post(
            TEST_PREFIX_HOST + "suggest_team/",
            data=json.dumps({"name": team.name}),
            content_type="application/json",
        )

        second_response = self.client.post(
            TEST_PREFIX_HOST + "suggest_team/",
            data=json.dumps({"name": team.name[:3]}),
            content_type="application/json",
        )

        third_response = self.client.post(
            TEST_PREFIX_HOST + "suggest_team/",
            data=json.dumps({"name": "Wrong name"}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(third_response.status_code, 400)

        self.assertEqual(first_response.data["name"], team.name)
        self.assertEqual(first_response.data["description"], team.description)

        self.assertEqual(second_response.data["name"], team.name)
        self.assertEqual(second_response.data["description"], team.description)


class TestTeamsView(UnitTest):
    @patch("teams.views.Timestamp.GetCurrentTime")
    @patch("teams.views.Timestamp.__init__", return_value=None)
    @patch("teams.views.notifications_client.Notify")
    def test_post(
        self,
        mock_notifications_client_Notify: Mock,
        mock_timestamp__init__: Mock,
        mock_timestamp_GetCurrentTime: Mock,
    ) -> None:
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        mock_timestamp_GetCurrentTime.return_value = timestamp

        admin = User.objects.create_user(**user_data)
        Profile.objects.create(user=admin)
        ConfirmEmail.objects.create(
            code="123456",
            user=admin,
            confirmed=True,
        )

        token = Token.objects.create(user=admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        team_data = {
            "name": "Название",
            "description": "Описание отсутствует.",
            "image": SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        }

        response = self.client.post(
            TEST_PREFIX_HOST + "teams/",
            data=team_data,
        )

        self.assertEqual(response.status_code, 201)

        created_team = Team.objects.all()[0]
        self.assertEqual(created_team.name, team_data["name"])
        self.assertEqual(created_team.description, team_data["description"])

        mock_notifications_client_Notify.assert_called_once_with(
            NotificationRequest(
                text=f'Команда "{team_data["name"]}" была успешна создана.',
                image=admin.profile.image.url,
                time=timestamp,
                tokens=[token.key],
            )
        )


class TestLeaveTeamView(UnitTest):
    def test_put(self) -> None:
        admin = User.objects.create_user(**user_data)

        updated_user_data = user_data.copy()
        updated_user_data["email"] = "email1@email.com"
        updated_user_data["username"] = "username1"

        teammate = User.objects.create_user(**updated_user_data)

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
        )

        teammate.profile.team = team
        teammate.profile.save()

        token = Token.objects.create(user=teammate)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.put(TEST_PREFIX_HOST + "leave_team/")

        self.assertEqual(response.status_code, 200)

        leaved_user = User.objects.get(username="username1")
        self.assertIsNone(leaved_user.profile.team)
