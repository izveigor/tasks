from tests.unit_tests.base import UnitTest
from users.methods import suggest_username
from django.contrib.auth import get_user_model

User = get_user_model()


class TestMethods(UnitTest):
    user_data = {
        "first_name": "first name",
        "last_name": "last name",
        "password": "password",
        "email": "email@email.com",
    }

    def test_suggest_username_if_username_without_digits(self):
        User.objects.create_user(
            username="username",
            **self.user_data,
        )
        suggested_username = suggest_username(username="username")
        self.assertEqual(suggested_username, "username1")

    def test_suggest_username_if_username_are_digits(self):
        suggested_username = suggest_username(username="123123")
        self.assertIsNone(suggested_username)

    def test_suggest_username_without_blanks(self):
        for index in range(1, 5):
            User.objects.create_user(
                username="username" + str(index),
                **self.user_data,
            )

        for index in range(1, 5):
            suggested_username = suggest_username("username" + str(index))
            self.assertEqual(suggested_username, "username5")

    def test_suggest_username_with_blanks(self):
        for index in range(1, 4):
            User.objects.create_user(
                username="username" + str(index),
                **self.user_data,
            )

        for index in range(5, 7):
            User.objects.create_user(
                username="username" + str(index),
                **self.user_data,
            )

        for index in range(1, 7):
            if index == 4:
                continue

            suggested_username = suggest_username("username" + str(index))
            self.assertEqual(suggested_username, "username4")
