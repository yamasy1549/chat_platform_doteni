from flask import Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
from flaskr.core import db
from flaskr.models import User
from flaskr.views import login_required


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    [GET] /auth/login
    [POST] /auth/login

    ログイン
    """

    if request.method == "POST":
        user, authenticated = User.authenticate(db.session.query, request.form["name"], request.form["password"])

        if authenticated:
            current_app.logger.info(f"[/auth/login] {user}")

            session["user_id"] = user.id
            flash("ログインしました")
            return redirect(url_for("index.root"))
        else:
            flash("ユーザ名かパスワードが違います。")

    return render_template("auth/login.html")

@bp.route("/logout")
@login_required
def logout():
    """
    [GET] /auth/logout

    ログアウト
    """

    current_app.logger.info(f"[/auth/logout] {g.user}")

    session.pop("user_id", None)
    flash("ログアウトしました")
    return redirect(url_for("index.root"))
