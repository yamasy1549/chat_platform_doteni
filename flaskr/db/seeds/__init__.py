import os
from flaskr import app
from flaskr.core import db
from flaskr.models.user import User
from flaskr.models.entry import Entry
from flaskr.db.seeds.entry import entries
from flaskr.db.seeds.user import users

def init_db_with_seeds():
    if os.path.exists("flaskr/flaskr.db"):
        os.remove("flaskr/flaskr.db")

    with app.app_context():
        db.create_all()
        db.session.bulk_save_objects([Entry(title=d[0], text=d[1]) for d in entries])
        db.session.bulk_save_objects([User(name=d[0], password=d[1]) for d in users])
        db.session.commit()

    print("データベースを初期化しました。")
