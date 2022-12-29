from django.conf import settings
from django.db import models


class Team(models.Model):  # type: ignore
    name = models.CharField("Название команды:", max_length=30, unique=True)
    description = models.TextField("Описание команды:", max_length=1500)
    image = models.ImageField("Изображение команды:", upload_to="images")
    admin = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
