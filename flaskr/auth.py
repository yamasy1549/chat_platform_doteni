import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    [GET] /auth/register
    [POST] /auth/register

    username, password を受け取ってユーザ新規登録をする
    """

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "ユーザ名が必須です。"
        elif not password:
            error = "パスワードが必須です。"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"ユーザ「{username}」はすでに登録されています。"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")

@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    [GET] /auth/login
    [POST] /auth/login

    username, password を受け取ってログインする
    session["user_id"] にユーザIDを保持しておく
    """

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "ユーザ名が違います。"
        elif not check_password_hash(user["password"], password):
            error = "パスワードが違います。"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    """
    [GET] /auth/logout

    ログアウトする
    sessionを空にする
    """

    session.clear()
    return redirect(url_for("index"))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()

def login_required(view):
    """
    このannotationがついた処理はログインが必須になる
    ログインしていなければ /auth/login へ、ログインしていればリクエスト先のページへ遷移する
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
