from rest_framework import permissions
from users.models import ConfirmEmail
from teams.models import Team


class EmailPermission(permissions.BasePermission):
    """
    Проверяем, проверен ли у пользователя email.
    """

    def has_permission(self, request, view):
        email = request.user.confirm_email
        return email.confirmed


class AdminTeamPermission(permissions.BasePermission):
    """
    Проверяем, что пользователем является администратором команды.
    """

    def has_permission(self, request, view):
        request.team = request.user.profile.team
        if request.team is None:
            return False
        if request.user == request.team.admin:
            return True
        return False


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
        request.team = request.user.profile.team
        if request.team is None:
            return False

        if request.user == request.team.admin:
            return True
        else:
            subordinates = request.user.profile.get_subordinates()
            if subordinates:
                return True
            return False
