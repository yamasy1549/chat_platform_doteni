import os
import tempfile

import pytest
from flaskr.factory import create_app
from flaskr.core import db
from flaskr.models import Room, User, Scenario

from tests.db.seeds.room import rooms
from tests.db.seeds.user import users
from tests.db.seeds.scenario import scenarios
from tests.db.seeds.room_scenario import room_scenarios


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
        db.session.bulk_save_objects([Room(name=d[0], status=d[1]) for d in rooms])
        db.session.bulk_save_objects([User(name=d[0], role=d[1], password=d[2]) for d in users])
        db.session.bulk_save_objects([Scenario(title=d[0], text=d[1]) for d in scenarios])

        for room_id, scenario_id in room_scenarios:
            room = Room.query.get(room_id)
            scenario = Scenario.query.get(scenario_id)
            room.scenarios.append(scenario)
            db.session.add(room)

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
