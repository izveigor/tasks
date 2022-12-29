from typing import Any

from celery import Celery
from flask import Flask

from constants import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
    __name__,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
)


def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        backend=CELERY_RESULT_BACKEND,
        broker=CELERY_BROKER_URL,
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):  # type: ignore
        def __call__(self, *args: Any, **kwargs: dict[str, Any]) -> Any:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
