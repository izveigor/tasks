from celery import Celery
from .constants import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery = Celery(
    __name__,
    backend=CELERY_RESULT_BACKEND,
    broker=CELERY_BROKER_URL,
)


def make_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
