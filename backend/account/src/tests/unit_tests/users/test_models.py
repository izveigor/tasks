from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from account.constants import EXPIRY_TIME, MAX_AVAILABLE_TRIES
from tests.helpers import check_model_fields, create_user
from tests.unit_tests.base import UnitTest
from users.models import ConfirmEmail, Profile, Team
from typing import Any

User = get_user_model()


class ModelsTest(UnitTest):
    user_data = {
        "first_name": "first_name",
        "last_name": "last_name",
        "username": "username",
        "email": "email@email.com",
        "password": "password",
    }

    def test_user(self) -> None:
        user_data_for_check: dict[str, Any] = {
            "last_login": None,
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            **self.user_data,
        }

        user_data_for_check.pop("password")

        create_user(self.user_data)
        check_model_fields(
            self,
            User.objects.all()[0],
            user_data_for_check,
            "password",
            "date_joined",
        )

    def test_profile(self) -> None:
        user = create_user(self.user_data)
        profile_data = {
            "user_id": user.id,
            "team_id": None,
            "supervisor_id": None,
            "job_title": "Разработчик ПО",
            "description": "Занимаюсь разработкой больше 3 лет.",
        }

        Profile.objects.create(
            **profile_data,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        check_model_fields(self, Profile.objects.all()[0], profile_data, "image")

    def test_confirm(self) -> None:
        user = create_user(self.user_data)
        confirm_data = {
            "user_id": user.id,
            "code": "123456",
            "expiry": EXPIRY_TIME,
            "available_tries": MAX_AVAILABLE_TRIES,
            "confirmed": False,
        }

        ConfirmEmail.objects.create(
            **confirm_data,
        )

        check_model_fields(self, ConfirmEmail.objects.all()[0], confirm_data)

    def test_supervisor(self) -> None:
        first_user = User.objects.create_user(
            first_name="first_name",
            last_name="last_name",
            username="username",
            email="email@email.com",
            password="password",
        )

        second_user = User.objects.create_user(
            first_name="first_name",
            last_name="last_name",
            username="username1",
            email="email@email.com",
            password="password",
        )

        third_user = User.objects.create_user(
            first_name="first_name",
            last_name="last_name",
            username="username2",
            email="email@email.com",
            password="password",
        )

        fourth_user = User.objects.create_user(
            first_name="first_name",
            last_name="last_name",
            username="username3",
            email="email@email.com",
            password="password",
        )

        fifth_user = User.objects.create_user(
            first_name="first_name",
            last_name="last_name",
            username="username5",
            email="email@email.com",
            password="password",
        )

        supervisor = User.objects.create_user(
            first_name="first_name",
            last_name="last_name",
            username="username4",
            email="email@email.com",
            password="password",
        )

        Profile.objects.create(
            user=first_user,
            supervisor=supervisor,
        )

        Profile.objects.create(
            user=second_user,
            supervisor=supervisor,
        )

        Profile.objects.create(
            user=third_user,
            supervisor=first_user,
        )

        Profile.objects.create(
            user=fourth_user,
            supervisor=second_user,
        )

        Profile.objects.create(
            user=fifth_user,
            supervisor=None,
        )

        Profile.objects.create(
            user=supervisor,
        )

        self.assertEqual(
            supervisor.profile.get_subordinates(),
            [first_user, third_user, second_user, fourth_user],
        )
