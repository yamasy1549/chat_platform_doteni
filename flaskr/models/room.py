import enum
from sqlalchemy.orm import synonym, validates
from hashlib import sha256
from flaskr.core import db
from flaskr.models.error import ValidationError


class Status(enum.Enum):
    UNAVAILABLE = 1
    AVAILABLE = 2
    OCCUPIED = 3
    USED = 4


class Room(db.Model):
    __tablename__ = "rooms"

    id     = db.Column("id",     db.Integer,    primary_key=True)
    status = db.Column("status", db.Enum(Status), nullable=False,   default=Status.UNAVAILABLE.name)

    @property
    def hash(self):
        value = str(self.id).encode()
        return sha256(value).hexdigest()

    hash = synonym("id", descriptor=hash)

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
