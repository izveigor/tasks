from django.test import TestCase
from django.db.models import Model
from typing import Any
from django.contrib.auth.models import User


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
