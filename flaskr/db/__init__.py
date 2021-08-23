import os
from flaskr import app
from flaskr.core import db
from flaskr.models import Room, Scenario, User, Message
import flaskr.db.seeds as seed


def init_db():
    database_file_path = "flaskr/{}".format(app.config["SQLALCHEMY_DATABASE_FILE"])

    if os.path.exists(database_file_path):
        os.remove(database_file_path)

    with app.app_context():
        db.create_all()


def init_db_with_seeds():
    init_db()

    with app.app_context():
        db.session.bulk_save_objects([Room(name=d[0], status=d[1]) for d in seed.rooms])
        db.session.bulk_save_objects([Scenario(title=d[0], text=d[1], displayname=d[2]) for d in seed.scenarios])
        db.session.bulk_save_objects([User(name=d[0], role=d[1], password=d[2]) for d in seed.users])
        db.session.bulk_save_objects([Message(text=d[0], room_id=d[1], user_id=d[2]) for d in seed.messages])

        for room_id, scenario_id in seed.room_scenarios:
            room = Room.query.get(room_id)
            scenario = Scenario.query.get(scenario_id)
            room.scenarios.append(scenario)
            db.session.add(room)

        db.session.commit()

    print("データベースを初期化しました。")
