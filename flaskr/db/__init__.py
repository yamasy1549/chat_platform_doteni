import os
from flaskr import app
from flaskr.core import db
from flaskr.models import Room, User, Scenario, Message
from flaskr.db.seeds.room import rooms
from flaskr.db.seeds.user import users
from flaskr.db.seeds.scenario import scenarios
from flaskr.db.seeds.message import messages
from flaskr.db.seeds.room_scenario import room_scenarios


def init_db():
    if os.path.exists("flaskr/flaskr.db"):
        os.remove("flaskr/flaskr.db")

    with app.app_context():
        db.create_all()


def init_db_with_seeds():
    init_db()

    with app.app_context():
        db.session.bulk_save_objects([Room(status=d[0]) for d in rooms])
        db.session.bulk_save_objects([User(name=d[0], role=d[1], password=d[2]) for d in users])
        db.session.bulk_save_objects([Scenario(title=d[0], text=d[1]) for d in scenarios])
        db.session.bulk_save_objects([Message(text=d[0], room_id=d[1], user_id=d[2]) for d in messages])

        for room_id, scenario_id in room_scenarios:
            room = Room.query.get(room_id)
            scenario = Scenario.query.get(scenario_id)
            room.scenarios.append(scenario)
            db.session.add(room)

        db.session.commit()

    print("データベースを初期化しました。")
