from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flaskr.core import db
from flaskr.models import User
from flaskr.views import login_required


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/")
@login_required
def index():
    """
    [GET] /users

    ユーザの一覧
    """

    users = User.query.all()
    return render_template("users/index.html", users=users)

@bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
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
        user.email = request.form["email"]
        user.password = request.form["password"]
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("users.index"))
    return render_template("users/edit.html", user=user)

@bp.route("/create", methods=["GET", "POST"])
def create():
    """
    [GET] /users/create
    [POST] /users/create

    ユーザの新規作成
    """

    if request.method == "POST":
        if request.form["name"] is "":
            flash("名前を入力してください。")
            return redirect(url_for("users.create"))

        if request.form["email"] is "":
            flash("メールアドレスを入力してください。")
            return redirect(url_for("users.create"))

        if request.form["password"] is "":
            flash("パスワードを入力してください。")
            return redirect(url_for("users.create"))

        if len(request.form["password"]) < 1:
            flash("パスワードは1文字以上にしてください。")
            return redirect(url_for("users.create"))

        try:
            user = User(name=request.form["name"],
                        email=request.form["email"],
                        password=request.form["password"])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        except:
            flash("メールアドレスはすでに登録されています。")
            return redirect(url_for("users.create"))
    return render_template("users/edit.html")

@bp.route("/<int:user_id>/delete", methods=["POST"])
@login_required
def delete(user_id):
    """
    [POST] /users/:user_id/delete

    ユーザの削除
    """

    user = User.query.get(user_id)
    if user is None:
        response = jsonify({"status": "Not Found"})
        response.status_code = 404
        return response
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("users.index"))
