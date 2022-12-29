import re

from django.contrib.auth import get_user_model
from typing import Optional

User = get_user_model()

DIGITS_PATTERN = "^[0-9]+$"
DIGIT_PATTERN = "[0-9]"


def suggest_username(username: str) -> Optional[str]:
    if re.match(DIGITS_PATTERN, username):
        return None

    excess_length = 0
    for char in username[::-1]:
        if re.match(DIGIT_PATTERN, char):
            excess_length += 1
        else:
            break

    username_without_digits = username[: len(username) - excess_length]

    users = User.objects.filter(username__contains=username_without_digits).order_by(
        "username"
    )
    if username_without_digits == username:
        return username + "1"

    for counter, user in enumerate(users, start=1):
        try:
            number = int(user.username[len(username_without_digits) :])
        except ValueError:
            continue
        else:
            if number != counter:
                return username_without_digits + str(counter)
    else:
        return username_without_digits + str(counter + 1)
