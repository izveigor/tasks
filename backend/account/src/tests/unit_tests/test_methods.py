from .base import UnitTest
from django.contrib.auth.models import User
from users.methods import suggest_username


class TestMethods(UnitTest):
    def test_suggest_username_if_username_are_digits(self):
        suggested_username = suggest_username(username="123123")
        self.assertIsNone(suggested_username)

    def test_suggest_username_without_blanks(self):
        for index in range(4, 0, -1):
            User.objects.create_user(
                username="username" + str(index),
                first_name="first name",
                last_name="last name",
                password="password",
                email="email@email.com",
            )

        suggested_username = suggest_username("username1")
        self.assertEqual(suggested_username, "username5")

    def test_suggest_username_with_blanks(self):
        for index in range(1, 4):
            User.objects.create_user(
                username="username" + str(index),
                first_name="first name",
                last_name="last name",
                password="password",
                email="email@email.com",
            )

        for index in range(5, 7):
            User.objects.create_user(
                username="username" + str(index),
                first_name="first name",
                last_name="last name",
                password="password",
                email="email@email.com",
            )

        suggested_username = suggest_username("username1")
        self.assertEqual(suggested_username, "username4")
