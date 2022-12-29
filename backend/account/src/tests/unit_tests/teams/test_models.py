from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from teams.models import Team
from tests.helpers import check_model_fields, create_user
from tests.unit_tests.base import UnitTest
from typing import Any


class TestTeamsModels(UnitTest):
    user_data: dict[str, Any] = {
        "first_name": "first_name",
        "last_name": "last_name",
        "username": "username",
        "email": "email@email.com",
        "password": "password",
    }

    def test_team(self) -> None:
        admin = create_user(self.user_data)
        team_data: dict[str, Any]= {
            "name": "Команда1",
            "description": "Мы первая команда!",
            "admin_id": admin.id,
        }

        Team.objects.create(
            **team_data,
            image=SimpleUploadedFile(
                name="default.png",
                content=open(settings.MEDIA_ROOT + "/" + "default.png", "rb").read(),
                content_type="image/png",
            ),
        )

        check_model_fields(
            self,
            Team.objects.all()[0],
            team_data,
            "image",
        )
