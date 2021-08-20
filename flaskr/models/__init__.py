from flaskr.core import db


class ValidationError(Exception):
    pass


def init():
    db.create_all()
