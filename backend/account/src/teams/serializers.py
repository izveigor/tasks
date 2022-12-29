from rest_framework import serializers

from .models import Team
from typing import Any


class TeamNameSerializer(serializers.Serializer):  # type: ignore
    name = serializers.CharField(max_length=30)


class TeamSerializer(serializers.ModelSerializer):  # type: ignore
    class Meta:
        model = Team
        fields = ["name", "description", "image"]


class CreateTeamSerializer(serializers.ModelSerializer):  # type: ignore
    class Meta:
        model = Team
        fields = ["name", "description", "image"]

    def validate(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        name = kwargs.get("name")
        description = kwargs.get("description")
        msg = ""
        if not name:
            msg = "Имя команды не должно быть пустым"
        elif Team.objects.filter(name=name).exists():
            msg = "Имя команды уже используется"
        elif not description:
            description = "Описание отсутствует."

        if msg:
            raise serializers.ValidationError(msg)

        return kwargs
