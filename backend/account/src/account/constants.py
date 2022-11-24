import datetime
import os
from django.conf import settings

MAX_AVAILABLE_TRIES: int = 3
EXPIRY_TIME = datetime.time(23, 59)

DEFAULT_PROFILE_JOB_TITLE = "отсутствует"
DEFAULT_PROFILE_DESCRIPTION = "Описание отсутствует."
DEFAULT_PROFILE_IMAGE = "default.png"

NOTIFICATIONS_HOST = os.environ.get("NOTIFICATIONS_HOST")
TASKS_HOST = os.environ.get("TASKS_HOST")
USERS_HOST = os.environ.get("USERS_HOST")

FRONTEND_HOST = "localhost:3000"
PREFIX_HOST = "account/"
TEST_PREFIX_HOST = "/account/"
