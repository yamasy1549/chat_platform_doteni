import os
from flaskr.core import db
from flaskr.db.seeds.entry import entries
from flaskr.db.seeds.user import users

def init_db_with_seeds():
    os.remove("flaskr/flaskr.db")
    db.create_all()

    db.session.bulk_save_objects(entries)
    db.session.bulk_save_objects(users)
    db.session.commit()

    print("データベースを初期化しました。")
