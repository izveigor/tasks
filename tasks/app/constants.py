from typing import Optional, Any


POSTGRESQL_SETTINGS = {
    "POSTGRES_HOST": "localhost",
    "POSTGRES_PORT": 5432,
    "POSTGRES_DB": "task",
    "POSTGRES_USER": "admin",
    "POSTGRES_PASSWORD": "password",
}

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

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
