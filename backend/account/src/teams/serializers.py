from rest_framework import serializers
from .models import Team


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name"]
