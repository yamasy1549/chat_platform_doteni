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
    AVAILABLE   = 2
    OCCUPIED    = 3
    USED        = 4

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
    name    = db.Column("name",    db.String(100),  nullable=False,   default="")
    status  = db.Column("status",  db.Enum(Status), nullable=False,   default=Status.UNAVAILABLE)
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
            value = Status.UNAVAILABLE

        if type(value) == Status:
            return value

        try:
            value = int(value)
            value = Status(value)
        except ValueError:
            raise ValidationError("ステータスの値を正しく指定してください。")

        return value

    def __repr__(self):
        return "<Room id={self.id} name={self.name!r} status={self.status!r}>".format(self=self)

    def capacity(self):
        """
        持っているシナリオの数（入室できるユーザの数）

        Return
        ------
        int
        """

        scenarios = self.scenarios
        return len(scenarios)

    def is_over_capacity(self):
        """
        もう入室できるユーザがいないかどうか

        Return
        ------
        bool
        """

        return len(self.users) >= self.capacity()

    def include(self, user):
        """
        ユーザを入室許可する

        Paramaters
        ----------
        user (User) : 入室を許可するユーザ

        Return
        ------
        Room
        """

        if user in self.users:
            return self

        if user.has_occupied_room():
            raise Exception("すでに使用中のルームがあります。使用中のルームを閉じてから、新しいルームに入ってください。")

        if self.is_over_capacity():
            raise Exception("ルームは満員です。")
        else:
            self.users.append(user)

            if self.is_over_capacity():
                self.status = Status.OCCUPIED

            db.session.add(self)
            db.session.commit()

            return self

    def fetch_scenario_of(self, user):
        """
        ユーザに対応するシナリオを取得する

        Paramaters
        ----------
        user (User) : シナリオを取得したいユーザ

        Return
        ------
        Scenario
        """

        if user not in self.users:
            raise Exception("不正な操作です。")

        index = self.users.index(user)
        return self.scenarios[index]
