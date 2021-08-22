from functools import wraps
from flask import g, redirect, request, session, url_for
from flaskr.models import User


def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))

        return f(*args, **kwargs)

    return decorated_view

def admin_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))

        if not g.user.is_admin():
            return redirect(url_for("index.root"))

        return f(*args, **kwargs)

    return decorated_view

def load_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

def init_app(app):
    from flaskr.views import index, auth, rooms, users, scenarios, socketio

    app.before_request(load_user)

    app.register_blueprint(index.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(rooms.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(scenarios.bp)
