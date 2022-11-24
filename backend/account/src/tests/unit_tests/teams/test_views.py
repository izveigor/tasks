from tests.unit_tests.base import UnitTest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from users.models import ConfirmEmail, Profile
from teams.models import Team
from account.constants import TEST_PREFIX_HOST
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import json

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

        user_data["email"] = "email1@email.com"
        user_data["username"] = "username1"

        user = User.objects.create_user(**user_data)
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

        user_data["email"] = "email1@email.com"
        user_data["username"] = "username2"

        supervisor = User.objects.create_user(**user_data)
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
