import os
from flaskr import app
from flaskr.core import db
from flaskr.models import Room, User, Scenario
from flaskr.db.seeds.room import rooms
from flaskr.db.seeds.user import users
from flaskr.db.seeds.scenario import scenarios


def init_db_with_seeds():
    if os.path.exists("flaskr/flaskr.db"):
        os.remove("flaskr/flaskr.db")

    with app.app_context():
        db.create_all()
        db.session.bulk_save_objects([Room(status=d[0]) for d in rooms])
        db.session.bulk_save_objects([User(name=d[0], role=d[1], password=d[2]) for d in users])
        db.session.bulk_save_objects([Scenario(title=d[0], text=d[1]) for d in scenarios])
        db.session.commit()

    print("データベースを初期化しました。")
