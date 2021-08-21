from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flaskr.core import db
from flaskr.models import Room
from flaskr.models.error import ValidationError
from flaskr.views import login_required, admin_required


bp = Blueprint("rooms", __name__, url_prefix="/rooms")


@bp.route("/")
@login_required
def index():
    """
    [GET] /rooms

    ルームの一覧
    """

    rooms = Room.query.order_by(Room.id.desc()).all()
    return render_template("rooms/index.html", rooms=rooms)

@bp.route("/<int:room_id>", methods=["GET"])
@login_required
def show(room_id):
    """
    [GET] /rooms/:room_id
    [POST] /rooms/:room_id

    ルームの閲覧
    """

    room = Room.query.get(room_id)
    if room is None:
        abort(404)
    return render_template("rooms/show.html", room=room)

@bp.route("/<int:room_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(room_id):
    """
    [GET] /rooms/:room_id/edit
    [POST] /rooms/:room_id/edit

    ルームの編集
    """

    room = Room.query.get(room_id)
    if room is None:
        abort(404)
    if request.method == "POST":
        room.status = request.form["status"]
        db.session.add(room)
        db.session.commit()
        return redirect(url_for("rooms.index"))
    return render_template("rooms/edit.html", room=room)

@bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():
    """
    [GET] /rooms/create
    [POST] /rooms/create

    ルームの新規作成
    """

    if request.method == "POST":
        try:
            if "status" in request.form:
                room = Room(
                        status=request.form["status"],
                        )
            else:
                room = Room()
            db.session.add(room)
            db.session.commit()
            flash("新しいRoomを作成しました")
            return redirect(url_for("rooms.index"))
        except ValidationError as error:
            flash(error.args[0])
            return redirect(url_for("rooms.create"))

    return render_template("rooms/edit.html")

@bp.route("/<int:room_id>/delete", methods=["POST"])
@admin_required
def delete(room_id):
    """
    [POST] /rooms/:room_id/delete

    ルームの削除
    """

    room = Room.query.get(room_id)
    if room is None:
        response = jsonify({"status": "Not Found"})
        response.status_code = 404
        return response
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for("rooms.index"))
