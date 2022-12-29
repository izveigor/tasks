import re
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Any

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from account.constants import (
    DEFAULT_PROFILE_DESCRIPTION,
    DEFAULT_PROFILE_IMAGE,
    DEFAULT_PROFILE_JOB_TITLE,
    EXPIRY_TIME,
    MAX_AVAILABLE_TRIES,
)
from teams.models import Team


class User(AbstractUser):  # type: ignore
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Profile(models.Model):  # type: ignore
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    job_title = models.CharField(
        "Название работы:", max_length=50, default=DEFAULT_PROFILE_JOB_TITLE
    )
    description = models.TextField(
        "Описание:", max_length=1500, default=DEFAULT_PROFILE_DESCRIPTION
    )
    image = models.ImageField(
        "Изображение профиля:", upload_to="images", default=DEFAULT_PROFILE_IMAGE
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
    )
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subordinates",
        null=True,
    )

    def get_subordinates(self) -> list[User]:
        result: list[User] = []

        def _search(subordinates: Any) -> None:
            for profile in subordinates:
                user = profile.user
                result.append(user)
                user_subordinates = user.subordinates.all()
                if user_subordinates is not None:
                    _search(user_subordinates)
                else:
                    continue

        _search(self.user.subordinates.all())
        return result


class ConfirmEmail(models.Model):  # type: ignore
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="confirm_email",
    )
    code = models.CharField("Код:", max_length=6)
    expiry = models.TimeField("Срок истечения:", default=EXPIRY_TIME)
    available_tries = models.IntegerField(
        "Доступные попытки:", default=MAX_AVAILABLE_TRIES
    )
    confirmed = models.BooleanField("Подтверждено", default=False)
