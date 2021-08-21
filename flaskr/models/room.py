import enum
import uuid
from sqlalchemy.orm import validates
from flaskr.core import db
from flaskr.models.error import ValidationError
from flaskr.models.room_scenario import room_scenarios


def generate_hash_id():
    return uuid.uuid4().hex


class Status(enum.Enum):
    UNAVAILABLE = 1
    AVAILABLE = 2
    OCCUPIED = 3
    USED = 4


class Room(db.Model):
    __tablename__ = "rooms"

    id      = db.Column("id",      db.Integer,      primary_key=True)
    hash_id = db.Column("hash_id", db.String(100),  nullable=False,   default=generate_hash_id)
    status  = db.Column("status",  db.Enum(Status), nullable=False,   default=Status.UNAVAILABLE.name)
    scenarios = db.relationship("Scenario", secondary=room_scenarios, lazy="subquery", backref=db.backref("rooms", lazy=True))
    messages  = db.relationship("Message", backref="rooms", lazy=True)

    @validates("status")
    def validate_status(self, key, value):
        if not value:
            value = Status.UNAVAILABLE.value

        try:
            value = int(value)
            value = Status(value)
        except ValueError:
            raise ValidationError("ステータスの値を正しく指定してください。")

        return value.name

    def __repr__(self):
        return "<Room id={id} status={status!r}>".format(id=self.id, status=self.status)
