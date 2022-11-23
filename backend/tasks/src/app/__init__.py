import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from models import db

from .views import bp_views
from .serializers import bp_marhmallow
from connection.tasks_server import tasks_serve
from threading import Thread
from .celery import make_celery
from constants import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, POSTGRESQL_SETTINGS


def create_app(config: str = "PRODUCTION", **kwargs) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True if config == "TESTING" else False
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f'postgresql://{POSTGRESQL_SETTINGS["POSTGRES_USER"]}:{POSTGRESQL_SETTINGS["POSTGRES_PASSWORD"]}@{POSTGRESQL_SETTINGS["POSTGRES_HOST"]}:{POSTGRESQL_SETTINGS["POSTGRES_PORT"]}/{POSTGRESQL_SETTINGS["POSTGRES_DB"]}'
    app.app_context().push()
    db.init_app(app)
    CORS(app)
    app.register_blueprint(bp_views)
    app.register_blueprint(bp_marhmallow)
    make_celery(app)
    if config != "TESTING":
        db.create_all()
        thread = Thread(target=tasks_serve, args=(app,))
        thread.start()
    return app
