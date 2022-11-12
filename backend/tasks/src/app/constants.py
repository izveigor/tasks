from typing import Optional, Any
import os


POSTGRESQL_SETTINGS = {
    "POSTGRES_HOST": os.environ.get("POSTGRES_HOST"),
    "POSTGRES_PORT": os.environ.get("POSTGRES_PORT"),
    "POSTGRES_DB": os.environ.get("POSTGRES_DB"),
    "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
}

REDIS_SETTINGS = {
    "REDIS_HOST": os.environ.get("REDIS_HOST", ""),
    "REDIS_PORT": os.environ.get("REDIS_PORT", ""),
}

CELERY_BROKER_URL = f'redis://{REDIS_SETTINGS["REDIS_HOST"]}:{REDIS_SETTINGS["REDIS_PORT"]}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_SETTINGS["REDIS_HOST"]}:{REDIS_SETTINGS["REDIS_PORT"]}'

TASK_STATUS = (
    "Успешно",
    "Обработка",
    "Закрыто",
)
DEFAULT_TASK_STATUS: str = "Обработка"
PROCESSING_TASK_STATUS: str = "Обработка"

NOTIFICATIONS_HOST = "localhost:50053"
TASKS_HOST = "localhost:50052"
USERS_HOST = "localhost:50051"

TASKS_NUMBER_FOR_PAGE = 10
PREFIX_HOST = "/tasks"
