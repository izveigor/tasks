from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Model
from django.test import TestCase

User = get_user_model()


def check_model_fields(
    self: TestCase, model: Model, data: dict[str, Any], *args: str
) -> None:
    fields: dict[str, Any] = vars(model)
    fields.pop("_state")
    fields.pop("id")

    for delete_field in args:
        fields.pop(delete_field)

    for key in fields.keys():
        self.assertEqual(fields[key], data[key])


def create_user(user_data: dict[str, Any]) -> Any:
    user = User.objects.create_user(
        **user_data,
    )

    return user
