from flask import Blueprint, current_app, render_template, redirect, url_for, flash, session, request
from flaskr.core import db
from flaskr.models import User


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    [GET] /auth/login
    [POST] /auth/login

    ログイン
    """

    if request.method == "POST":
        user, authenticated = User.authenticate(db.session.query, request.form["email"], request.form["password"])
        if authenticated:
            session["user_id"] = user.id
            flash("ログインしました")
            current_app.logger.info(f"[/auth/login] {user}")
            return redirect(url_for("index.root"))
        else:
            flash("メールアドレスかパスワードが違います。")
    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    """
    [GET] /auth/logout

    ログアウト
    """

    session.pop("user_id", None)
    flash("ログアウトしました")
    return redirect(url_for("index.root"))
