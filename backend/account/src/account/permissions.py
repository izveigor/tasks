from rest_framework import permissions

from teams.models import Team
from users.models import ConfirmEmail
from typing import Any

class EmailPermission(permissions.BasePermission):  # type: ignore
    """
    Проверяем, проверен ли у пользователя email.
    """

    def has_permission(self, request: Any, view: Any) -> bool:
        email = request.user.confirm_email
        return email.confirmed  # type: ignore


class AdminTeamPermission(permissions.BasePermission):  # type: ignore
    """
    Проверяем, что пользователем является администратором команды.
    """

    def has_permission(self, request: Any, view: Any) -> bool:
        request.team = request.user.profile.team
        if request.team is None:
            return False
        if request.user == request.team.admin:
            return True
        return False


class TeamPermission(permissions.BasePermission):  # type: ignore
    """
    Проверяем, что пользователь состоит в команде
    """

    def has_permission(self, request: Any, view: Any) -> bool:
        if request.user.profile.team:
            request.team = request.user.profile.team
            return True
        return False


class CreatorTeamPermission(permissions.BasePermission):  # type: ignore
    """
    Проверяем, что пользователь может создать задание
    """

    def has_permission(self, request: Any, view: Any) -> bool:
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
