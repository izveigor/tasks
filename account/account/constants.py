import datetime
import os
from django.conf import settings

MAX_AVAILABLE_TRIES: int = 3
EXPIRY_TIME = datetime.time(23, 59)

DEFAULT_PROFILE_JOB_TITLE = "отсутствует"
DEFAULT_PROFILE_DESCRIPTION = "Описание отсутствует."
DEFAULT_PROFILE_IMAGE = "default.png"

NOTIFICATIONS_HOST = "localhost:50053"
TASKS_HOST = "localhost:50052"
USERS_HOST = "localhost:50051"

FRONTEND_HOST = "localhost:3000"
