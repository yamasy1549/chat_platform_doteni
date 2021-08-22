from flaskr.core import db


room_users = db.Table("room_users",
        db.Column("room_id", db.Integer, db.ForeignKey("rooms.id"), primary_key=True),
        db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
        )
