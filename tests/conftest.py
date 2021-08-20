import os
import tempfile

import pytest
from flaskr.factory import create_app
from flaskr.core import db
from flaskr.models.entry import Entry
from flaskr.models.user import User
from flaskr.models.scenario import Scenario

from tests.db.seeds.entry import entries
from tests.db.seeds.user import users
from tests.db.seeds.scenario import scenarios


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, name="test1", password="test1"):
        return self._client.post(
            "/auth/login",
            data={"name": name, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        "DEBUG": False,
        "TESTING": True,
        "SECRET_KEY": "secret key",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_POOL_SIZE": None,
        "SQLALCHEMY_POOL_TIMEOUT": None,
        "SQLALCHEMY_POOL_RECYCLE": None,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        db.session.bulk_save_objects([Entry(title=d[0], text=d[1]) for d in entries])
        db.session.bulk_save_objects([User(name=d[0], role=d[1], password=d[2]) for d in users])
        db.session.bulk_save_objects([Scenario(title=d[0], text=d[1]) for d in scenarios])
        db.session.commit()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
