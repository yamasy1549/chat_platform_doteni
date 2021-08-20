from sqlalchemy.orm import synonym, validates
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.core import db
from flaskr.models import ValidationError


class User(db.Model):
    __tablename__ = "users"

    id        = db.Column("id",       db.Integer,     primary_key=True)
    name      = db.Column("name",     db.String(100), nullable=False, unique=True)
    _password = db.Column("password", db.String(100), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        password = self.validate_password("password", password)
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym("_password", descriptor=password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValidationError("ユーザ名は必須です。")

        if User.query.filter(User.name == name).first():
            raise ValidationError("ユーザ名はすでに登録されています。")

        if len(name) < 3:
            raise ValidationError("ユーザ名は3文字以上にしてください。")

        return name

    @validates("password")
    def validate_password(self, key, password):
        if not password:
            raise ValidationError("パスワードは必須です。")

        if len(password) < 3:
            raise ValidationError("パスワードは3文字以上にしてください。")

        return password

    @classmethod
    def authenticate(cls, query, name, password):
        user = query(cls).filter(cls.name==name).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __repr__(self):
        return u"<User id={self.id} name={self.name!r}>".format(self=self)
