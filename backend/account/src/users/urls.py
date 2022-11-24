from django.urls import path
from users import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("register/", views.RegisterView.as_view()),
    path("change_username/", views.ChangeUsernameView.as_view()),
    path("change_password/", views.ChangePasswordView.as_view()),
    path("check_username/", views.CheckUsernameView.as_view()),
    path("check_email/", views.CheckEmailView.as_view()),

    path("authorization/", views.Authorization.as_view()),
    path("authorization_with_email/", views.AuthorizationWithEmail.as_view()),

    path("confirm_email/", views.ConfirmEmailView.as_view()),
    path("settings/", views.SettingsProfileView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    path("avatar/", views.AvatarView.as_view()),
    path("team/", views.TeamView.as_view()),
    path("teams/", views.TeamsView.as_view()),
    path("profile/<int:user_id>", views.ProfileView.as_view()),
    path("join/", views.JoinTeamView.as_view()),
    path("accept/", views.AcceptIntoTeamView.as_view()),
    path("group/", views.GroupView.as_view()),
    path("user_team/<str:username>", views.UserTeamView.as_view()),
    path("suggest_employee/", views.SuggestEmployeeView.as_view()),
    path("suggest_team/", views.SuggestTeamView.as_view()),
    path("leave_team/", views.LeaveTeamView.as_view()),
]
'''