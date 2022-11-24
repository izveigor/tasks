from rest_framework import serializers
from .models import Team


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name"]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name", "description", "image"]


class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name", "description", "image"]

    def validate(self, kwargs):
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
