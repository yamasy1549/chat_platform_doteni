from functools import wraps
from flask import session, g, redirect, url_for, request
from flaskr.models.user import User


def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        return f(*args, **kwargs)
    return decorated_view

def load_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session["user_id"])

def init_app(app):
    app.before_request(load_user)

    from flaskr.views import index, auth, entries, users
    app.register_blueprint(index.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(entries.bp)
    app.register_blueprint(users.bp)
