from sqlalchemy import or_
from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, session, url_for
from flaskr.core import db
from flaskr.models import Room, Scenario, Status, Message, User
from flaskr.models.error import ValidationError
from flaskr.views import login_required, admin_required


bp = Blueprint("rooms", __name__, url_prefix="/rooms")


def fetch_user():
    """
    Return
    ------
    User
    """

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    return user


def fetch_room_from_hash_id(hash_id):
    """
    Paramaters
    ----------
    hash_id (str) : ルームのhash_id

    Return
    ------
    Room
    """

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

    user = g.user

    if user.is_admin():
        rooms = Room.query.all()
    else:
        my_rooms = Room.query \
                .filter(or_(Room.status==Status.AVAILABLE, Room.status==Status.OCCUPIED)) \
                .join(Room.users, aliased=True).filter_by(id=user.id) \
                .all()
        available_rooms = Room.query.filter_by(status=Status.AVAILABLE).all()
        available_rooms = set(available_rooms) - set(my_rooms)
        rooms = sorted(set(available_rooms), key=lambda room: room.id)
        rooms = [*my_rooms, *rooms]

    return render_template("rooms/index.html", rooms=rooms)

@bp.route("/<string:hash_id>", methods=["GET"])
@login_required
def show(hash_id):
    """
    [GET] /rooms/:hash_id
    [POST] /rooms/:hash_id

    ルームの閲覧
    """

    user = g.user
    room = fetch_room_from_hash_id(hash_id)

    if room is None:
        abort(404)

    try:
        if user.is_admin():
            scenarios = room.scenarios
        else:
            if room.status == Status.USED:
                abort(404)

            room.include(user)
            scenarios = [room.fetch_scenario_of(user)]

        current_app.logger.info(f"[/rooms/{hash_id}] {user} {scenarios}")
        return render_template("rooms/show.html", room=room, scenarios=scenarios)

    except Exception as error:
        flash(error.args[0])

    return redirect(url_for("rooms.index"))

@bp.route("/<string:hash_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(hash_id):
    """
    [GET] /rooms/:hash_id/edit
    [POST] /rooms/:hash_id/edit

    ルームの編集
    """

    room = fetch_room_from_hash_id(hash_id)

    if room is None:
        abort(404)

    if request.method == "POST":
        try:
            if "scenarios" in request.form:
                room.scenarios = []
                for scenario_id in request.form.getlist("scenarios"):
                    scenario = Scenario.query.get(scenario_id)
                    room.scenarios.append(scenario)

            if "status" in request.form:
                room.status = request.form["status"]

            if "name" in request.form:
                room.name = request.form["name"]

            db.session.add(room)
            db.session.commit()

            current_app.logger.info(f"[/rooms/{hash_id}/edit] {room}")

        except ValidationError as error:
            flash(error.args[0])
            return redirect(url_for("rooms.edit", hash_id=hash_id))

        return redirect(url_for("rooms.index"))

    scenarios = Scenario.query.all()
    return render_template("rooms/edit.html", room=room, scenarios=scenarios)

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
            room = Room()

            if "scenarios" in request.form:
                room.scenarios = []
                for scenario_id in request.form.getlist("scenarios"):
                    scenario = Scenario.query.get(scenario_id)
                    room.scenarios.append(scenario)

            if "status" in request.form:
                room.status = request.form["status"]

            if "name" in request.form:
                room.name = request.form["name"]

            db.session.add(room)
            db.session.commit()

            current_app.logger.info(f"[/rooms/create] {room}")
            flash("新しいRoomを作成しました")
            return redirect(url_for("rooms.index"))

        except ValidationError as error:
            flash(error.args[0])
            return redirect(url_for("rooms.create"))

    scenarios = Scenario.query.all()
    return render_template("rooms/edit.html", scenarios=scenarios)

@bp.route("/<string:hash_id>/delete", methods=["POST"])
@admin_required
def delete(hash_id):
    """
    [POST] /rooms/:hash_id/delete

    ルームの削除
    """

    room = fetch_room_from_hash_id(hash_id)

    if room is None:
        abort(404)

    try:
        db.session.delete(room)
        db.session.commit()

        current_app.logger.info(f"[/rooms/{hash_id}/delete] {room}")
        return redirect(url_for("rooms.index"))

    except ValidationError as error:
        flash(error.args[0])
        return redirect(url_for("rooms.edit", hash_id=hash_id))
