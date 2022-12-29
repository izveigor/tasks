import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from sqlalchemy import text

from app import create_app
from models import db


@pytest.fixture()  # type: ignore
def testing_app() -> Flask:
    app: Flask = create_app("TESTING")
    db.create_all()
    yield app
    delete_task_user = text(
        """
            DROP TABLE task_user CASCADE;
        """
    )
    db.session.execute(delete_task_user)
    db.session.commit()
    db.drop_all()


@pytest.fixture()  # type: ignore
def client(testing_app: Flask) -> FlaskClient:
    return testing_app.test_client()


@pytest.fixture()  # type: ignore
def runner(testing_app: Flask) -> FlaskCliRunner:
    return testing_app.test_cli_runner()
