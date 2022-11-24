from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("authorization_like_teammate/", views.AuthorizationLikeTeammate.as_view()),
    path("authorization_like_admin/", views.AuthorizationLikeAdmin.as_view()),
    path("authorization_like_creator/", views.AuthorizationLikeCreator.as_view()),

    path("check_team_name/", views.CheckTeamNameView.as_view()),
    path("team/", views.TeamView.as_view()),
    path("join/", views.JoinTeamView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
