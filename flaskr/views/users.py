from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for
from flaskr.core import db
from flaskr.models import User
from flaskr.models.error import ValidationError
from flaskr.views import admin_required


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/")
@admin_required
def index():
    """
    [GET] /users

    ユーザの一覧
    """

    users = User.query.all()
    return render_template("users/index.html", users=users)

@bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(user_id):
    """
    [GET] /users/:user_id/edit
    [POST] /users/:user_id/edit

    ユーザの編集
    """

    user = User.query.get(user_id)

    if user is None:
        abort(404)

    if request.method == "POST":
        user.name = request.form["name"]
        user.password = request.form["password"]

        try:
            db.session.add(user)
            db.session.commit()

            current_app.logger.info(f"[/users/{user_id}/edit] {user}")
            return redirect(url_for("users.index"))

        except ValidationError as error:
            flash(error.args[0])
            return redirect(url_for("users.edit", user_id=user_id))

    return render_template("users/edit.html", user=user)

@bp.route("/create", methods=["GET", "POST"])
def create():
    """
    [GET] /users/create
    [POST] /users/create

    ユーザの新規作成
    """

    if request.method == "POST":
        try:
            if "role" in request.form:
                user = User(name=request.form["name"],
                        role=request.form["role"],
                        password=request.form["password"])
            else:
                user = User(name=request.form["name"],
                        password=request.form["password"])

            db.session.add(user)
            db.session.commit()

            current_app.logger.info(f"[/users/create] {user}")

            if session.get("user_id"):
                return redirect(url_for("users.index"))
            else:
                return redirect(url_for("index.root"))

        except ValidationError as error:
            flash(error.args[0])
            return redirect(url_for("users.create"))

    return render_template("users/edit.html")

@bp.route("/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete(user_id):
    """
    [POST] /users/:user_id/delete

    ユーザの削除
    """

    user = User.query.get(user_id)

    if user is None:
        abort(404)

    try:
        db.session.delete(user)
        db.session.commit()

        current_app.logger.info(f"[/users/{user_id}/delete] {user}")
        return redirect(url_for("users.index"))

    except ValidationError as error:
        flash(error.args[0])
        return redirect(url_for("users.edit", user_id=user_id))
