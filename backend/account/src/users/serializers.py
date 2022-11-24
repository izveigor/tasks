from .models import Profile, ConfirmEmail
from teams.models import Team
from rest_framework import serializers
from django.contrib.auth import authenticate
from .methods import suggest_username
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")

        if not username:
            msg = "Имя пользователя не должно быть пустым"
            raise serializers.ValidationError(msg, code="authorization")
        elif not password:
            msg = "Пароль не должен быть пустым"
            raise serializers.ValidationError(msg, code="authorization")
        else:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if user is None:
                msg = "Неправильное имя пользователя или пароль"
                raise serializers.ValidationError(msg, code="authorization")

        kwargs["user"] = user
        return kwargs


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def validate(self, kwargs):
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        username = kwargs.get("username")
        email = kwargs.get("email")
        password = kwargs.get("password")
        msg = ""

        if not first_name:
            msg = "Имя не должно быть пустым"
        elif not last_name:
            msg = "Фамилия на должна быть пустой"
        elif not username:
            msg = "Имя пользователя не должно быть пустым"
        elif not email:
            msg = "Электронный адрес не должен быть пустым"
        elif not password:
            msg = "Пароль не должен быть пустым"

        if User.objects.filter(username=username).exists():
            msg = "Пользователь с таким именем пользователем уже существует"

        if User.objects.filter(email=email).exists():
            msg = "Пользователь с таким Электронным адресом уже существует"

        if msg:
            raise serializers.ValidationError(msg)

        kwargs["user"] = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        return kwargs


class ChangeUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

    def validate(self, kwargs):
        username = kwargs.get("username")
        msg = ""
        if not username:
            msg = "Имя пользователя не должно быть пустым"
        elif User.objects.filter(username=username).exists():
            available_username = suggest_username(username)
            if available_username:
                msg = f'Такое имя пользователя уже существует! Доступное имя: "{available_username}".'
            else:
                msg = "Такое имя пользователя уже существует!"

        if msg:
            raise serializers.ValidationError(msg)

        return kwargs


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    def validate(self, kwargs):
        password = kwargs.get("password")
        repeated_password = kwargs.get("repeated_password")
        msg = ""

        if not password:
            msg = "Пароль не должен быть пустым"
        elif not repeated_password:
            msg = "Повторный пароль не должен быть пустым"
        elif password != repeated_password:
            msg = "Пароль должен совпадать с повторным паролем"

        if msg:
            raise serializers.ValidationError(msg)

        return kwargs


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class EmailAvailableTriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmEmail
        fields = ["available_tries"]


class EmailCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmEmail
        fields = ["code"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Profile
        fields = ["job_title", "description", "image", "user"]


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["image"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserWithImageSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Profile
        fields = ["image", "user"]


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


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name", "description", "image"]


class GroupPutSerializer(serializers.Serializer):
    supervisor_username = serializers.CharField(
        write_only=True,
    )

    subordinate_username = serializers.CharField(
        write_only=True,
    )

    def validate(self, kwargs):
        supervisor_username = kwargs.get("supervisor_username")
        subordinate_username = kwargs.get("subordinate_username")

        try:
            kwargs["supervisor_user"] = User.objects.get(username=supervisor_username)
        except User.DoesNotExist:
            return serializers.ValidationError(
                "Имя пользователя руководителя не было найдено."
            )

        try:
            kwargs["subordinate_user"] = User.objects.get(username=subordinate_username)
        except User.DoesNotExist:
            return serializers.ValidationError(
                "Имя пользователя подчиненного не было найдено."
            )

        return kwargs


class GroupDeleteSerializer(serializers.Serializer):
    username = serializers.CharField(
        write_only=True,
    )

    def validate(self, kwargs):
        username = kwargs.get("username")

        try:
            kwargs["user"] = User.objects.get(username=username)
        except User.DoesNotExist:
            return serializers.ValidationError("Имя пользователя не было найдено.")

        return kwargs
