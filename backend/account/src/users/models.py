from account.constants import (
    EXPIRY_TIME,
    MAX_AVAILABLE_TRIES,
    DEFAULT_PROFILE_IMAGE,
    DEFAULT_PROFILE_DESCRIPTION,
    DEFAULT_PROFILE_JOB_TITLE,
)
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import re
from enum import Enum
from dataclasses import dataclass


class Team(models.Model):
    name = models.CharField("Название команды:", max_length=30, unique=True)
    description = models.TextField("Описание команды:", max_length=1500)
    image = models.ImageField("Изображение команды:", upload_to="images")
    admin = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class Profile(models.Model):
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
        on_delete=models.CASCADE,
        null=True,
    )
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="supervisors",
        null=True,
    )

    def get_subordinates(self):
        result: list[User] = []

        def _search(supervisors):
            for profile in supervisors:
                user = profile.user
                result.append(user)
                user_supervisors = user.supervisors.all()
                if user_supervisors is not None:
                    _search(user_supervisors)
                else:
                    continue

        _search(self.user.supervisors.all())
        return result


class ConfirmEmail(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    code = models.CharField("Код:", max_length=6)
    expiry = models.TimeField("Срок истечения:", default=EXPIRY_TIME)
    available_tries = models.IntegerField(
        "Доступные попытки:", default=MAX_AVAILABLE_TRIES
    )
    confirmed = models.BooleanField("Подтверждено", default=False)
