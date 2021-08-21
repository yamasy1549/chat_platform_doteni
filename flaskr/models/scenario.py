from sqlalchemy.orm import validates
from flaskr.core import db
from flaskr.models.error import ValidationError


class Scenario(db.Model):
    __tablename__ = "scenarios"

    id    = db.Column("id",    db.Integer,      primary_key=True)
    title = db.Column("title", db.String(100),  nullable=False, unique=True)
    text  = db.Column("text",  db.String(5000), nullable=False)

    @validates("title")
    def validate_name(self, key, value):
        if not value:
            raise ValidationError("タイトルは必須です。")

        if Scenario.query.filter(Scenario.title == value).first():
            raise ValidationError("タイトルはすでに登録されています。")

        if len(value) < 1:
            raise ValidationError("タイトルは1文字以上にしてください。")

        return value

    def __repr__(self):
        return "<Scenario id={id} title={title!r}>".format(id=self.id, title=self.title)

