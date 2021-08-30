import datetime
from sqlalchemy import DateTime
from flaskr.core import db


class RoomUser(db.Model):
    __tablename__ = "room_users"

    room_id   = db.Column("room_id",   db.Integer, db.ForeignKey("rooms.id"), primary_key=True)
    user_id   = db.Column("user_id",   db.Integer, db.ForeignKey("users.id"), primary_key=True)
    timestamp = db.Column("timestamp", DateTime, default=datetime.datetime.utcnow)
