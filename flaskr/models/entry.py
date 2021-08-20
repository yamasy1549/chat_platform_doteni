from flaskr.core import db
from flaskr.models import ValidationError


class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    text = db.Column(db.Text)

    def __repr__(self):
        return "<Entry id={id} title={title!r}>".format(
                id=self.id, title=self.title)
