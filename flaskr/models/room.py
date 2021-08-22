import enum
import uuid
from sqlalchemy.orm import validates
from flaskr.core import db
from flaskr.models.error import ValidationError
from flaskr.models.room_scenario import room_scenarios
from flaskr.models.room_user import room_users


def generate_hash_id():
    return uuid.uuid4().hex


class Status(enum.Enum):
    UNAVAILABLE = 1
    AVAILABLE = 2
    OCCUPIED = 3
    USED = 4

    def to_text(self):
        if self == Status.UNAVAILABLE:
            return "使用不可"
        if self == Status.AVAILABLE:
            return "使用可"
        if self == Status.OCCUPIED:
            return "使用中"
        if self == Status.USED:
            return "使用済み"


class Room(db.Model):
    __tablename__ = "rooms"

    id      = db.Column("id",      db.Integer,      primary_key=True)
    hash_id = db.Column("hash_id", db.String(100),  nullable=False,   default=generate_hash_id)
    name    = db.Column("name",    db.String(100),  nullable=False)
    status  = db.Column("status",  db.Enum(Status), nullable=False,   default=Status.UNAVAILABLE.name)
    scenarios = db.relationship("Scenario", secondary=room_scenarios, lazy="subquery", backref=db.backref("rooms", lazy=True))
    users     = db.relationship("User",     secondary=room_users,     lazy="subquery", backref=db.backref("rooms", lazy=True))
    messages  = db.relationship("Message", backref="rooms", lazy=True)

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) == 0:
            value = "ルーム"

        return value

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
        return "<Room id={id} name={name!r} status={status!r}>".format(id=self.id, name=self.name, status=self.status)

    def capacity(self):
        scenarios = self.scenarios
        return len(scenarios)

    def is_over_capacity(self):
        return len(self.users) >= self.capacity()

    def join_user(self, user):
        if user in self.users:
            return True

        if self.is_over_capacity():
            raise Exception("ルームは満員です。")
        else:
            self.users.append(user)
            if self.capacity() == len(self.users):
                self.status = Status.OCCUPIED.value
            db.session.add(self)
            db.session.commit()
            print(self)
            return True

    def fetch_scenario_of(self, user):
        index = self.users.index(user)
        return self.scenarios[index]
