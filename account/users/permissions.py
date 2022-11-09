from rest_framework import permissions
from .models import ConfirmEmail, Team
from django.db.models import Q


class EmailPermission(permissions.BasePermission):
    """
    Проверяем, проверен ли у пользователя email.
    """

    def has_permission(self, request, view):
        try:
            email = ConfirmEmail.objects.get(user=request.user)
        except ConfirmEmail.DoesNotExist:
            return False

        return email.confirmed


class AdminTeamPermission(permissions.BasePermission):
    """
    Проверяем, что пользователем является администратором команды.
    """

    def has_permission(self, request, view):
        try:
            request.team = Team.objects.get(admin=request.user)
        except Team.DoesNotExist:
            return False
        else:
            return True


class TeamPermission(permissions.BasePermission):
    """
    Проверяем, что пользователь состоит в команде
    """

    def has_permission(self, request, view):
        if request.user.profile.team:
            request.team = request.user.profile.team
            return True
        return False


class CreatorTeamPermission(permissions.BasePermission):
    """
    Проверяем, что пользователь может создать задание
    """

    def has_permission(self, request, view):
        try:
            Team.objects.get(admin=request.user)
        except Team.DoesNotExist:
            subordinates = request.user.profile.get_subordinates()
            if subordinates:
                return True
            else:
                return False
        else:
            return True
