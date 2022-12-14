from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users import views

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
    path("avatar/", views.AvatarView.as_view()),
    path("group/", views.GroupView.as_view()),
    path("suggest_employee/", views.SuggestEmployeeView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
