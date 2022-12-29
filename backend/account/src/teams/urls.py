from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users import views

urlpatterns = [
    path("authorization_like_teammate/", views.AuthorizationLikeTeammate.as_view()),  # type: ignore
    path("authorization_like_admin/", views.AuthorizationLikeAdmin.as_view()),  # type: ignore
    path("authorization_like_creator/", views.AuthorizationLikeCreator.as_view()),  # type: ignore
    path("check_team_name/", views.CheckTeamNameView.as_view()),  # type: ignore
    path("team/", views.TeamView.as_view()),  # type: ignore
    path("join/", views.JoinTeamView.as_view()),  # type: ignore
    path("accept/", views.AcceptIntoTeamView.as_view()),  # type: ignore
    path("suggest_team/", views.SuggestTeamView.as_view()),  # type: ignore
    path("teams/", views.TeamsView.as_view()),  # type: ignore
    path("leave_team/", views.LeaveTeamView.as_view()),  # type: ignore
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
