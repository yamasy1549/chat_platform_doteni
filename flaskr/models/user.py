import enum
from sqlalchemy.orm import synonym, validates
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.core import db
from flaskr.models.error import ValidationError


class Role(enum.Enum):
    ADMIN = 1
    NORMAL = 2

    def to_text(self):
        if self == Role.ADMIN:
            return "管理者"
        if self == Role.NORMAL:
            return "利用者"


class User(db.Model):
    __tablename__ = "users"

    id        = db.Column("id",       db.Integer,     primary_key=True)
    name      = db.Column("name",     db.String(100), nullable=False, unique=True)
    role      = db.Column("role",     db.Enum(Role),  nullable=False,              default=Role.NORMAL.name)
    _password = db.Column("password", db.String(100), nullable=False)
    messages  = db.relationship("Message", backref="user", lazy=True)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        password = self.validate_password("password", password)
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym("_password", descriptor=password_descriptor)

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValidationError("ユーザ名は必須です。")

        if User.query.filter_by(name=value).first():
            raise ValidationError("ユーザ名はすでに登録されています。")

        if len(value) < 3:
            raise ValidationError("ユーザ名は3文字以上にしてください。")

        return value

    @validates("password")
    def validate_password(self, key, value):
        if not value:
            raise ValidationError("パスワードは必須です。")

        if len(value) < 3:
            raise ValidationError("パスワードは3文字以上にしてください。")

        return value

    @validates("role")
    def validate_role(self, key, value):
        if not value:
            value = Role.NORMAL.value

        try:
            value = int(value)
            value = Role(value)
        except ValueError:
            raise ValidationError("ロールの値を正しく指定してください。")

        return value.name

    @classmethod
    def authenticate(cls, query, name, password):
        user = query(cls).filter(cls.name==name).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.role == Role.ADMIN

    def __repr__(self):
        return u"<User id={self.id} name={self.name!r}>".format(self=self)
