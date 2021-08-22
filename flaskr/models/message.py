from sqlalchemy.orm import validates
from flaskr.core import db
from flaskr.models.error import ValidationError


class Message(db.Model):
    __tablename__ = "messages"

    id      = db.Column("id",       db.Integer,     primary_key=True)
    text    = db.Column("status",   db.String(100), nullable=False)
    room_id = db.Column("room_id",  db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    user_id = db.Column("user_id",  db.Integer, db.ForeignKey("users.id"), nullable=False)

    @validates("text")
    def validate_text(self, key, value):
        if not value:
            raise ValidationError("テキストは必須です。")

        if len(value) < 1:
            raise ValidationError("テキストは1文字以上にしてください。")

        return value

    def __repr__(self):
        return "<Message id={self.id} room_id={self.room_id} user_id={self.user_id} text={self.text!r}>".format(self=self)
