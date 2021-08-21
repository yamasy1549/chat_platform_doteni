from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request, abort
from flaskr.core import db
from flaskr.models import Room
from flaskr.models.error import ValidationError
from flaskr.views import login_required, admin_required


bp = Blueprint("rooms", __name__, url_prefix="/rooms")


def get_room_from_hash_id(hash_id):
    room_list = Room.query.filter_by(hash_id=hash_id).all()
    if len(room_list) == 0:
        return None
    return room_list[0]


@bp.route("/")
@login_required
def index():
    """
    [GET] /rooms

    ルームの一覧
    """

    rooms = Room.query.order_by(Room.id.desc()).all()
    return render_template("rooms/index.html", rooms=rooms)

@bp.route("/<string:hash_id>", methods=["GET"])
@login_required
def show(hash_id):
    """
    [GET] /rooms/:hash_id
    [POST] /rooms/:hash_id

    ルームの閲覧
    """

    room = get_room_from_hash_id(hash_id)
    if room is None:
        abort(404)
    return render_template("rooms/show.html", room=room)

@bp.route("/<string:hash_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(hash_id):
    """
    [GET] /rooms/:hash_id/edit
    [POST] /rooms/:hash_id/edit

    ルームの編集
    """

    room = get_room_from_hash_id(hash_id)
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

@bp.route("/<string:hash_id>/delete", methods=["POST"])
@admin_required
def delete(hash_id):
    """
    [POST] /rooms/:hash_id/delete

    ルームの削除
    """

    room = get_room_from_hash_id(hash_id)
    if room is None:
        response = jsonify({"status": "Not Found"})
        response.status_code = 404
        return response
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for("rooms.index"))
