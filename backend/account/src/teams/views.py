from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Team
from account.permissions import (
    EmailPermission,
    AdminTeamPermission,
    TeamPermission,
    CreatorTeamPermission,
)


class AuthorizationLikeTeammate(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, TeamPermission]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class AuthorizationLikeAdmin(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, AdminTeamPermission]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class AuthorizationLikeCreator(APIView):
    permission_classes = [IsAuthenticated, EmailPermission, CreatorTeamPermission]

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class CheckTeamNameView(APIView):
    def post(self, request, format=None):
        serializer = serializers.TeamNameSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=False)
        name = serializer.data["name"]
        response = {}
        if Team.objects.filter(name=name).exists():
            response["exist"] = True
        else:
            response["exist"] = False

        return Response(response, status=status.HTTP_200_OK)