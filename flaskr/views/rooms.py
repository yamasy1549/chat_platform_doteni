from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request, abort, g, session
from flask_socketio import emit, join_room, leave_room
from flaskr.factory import socketio
from flaskr.core import db
from flaskr.models import Room, Scenario, Status, Message, User
from flaskr.models.error import ValidationError
from flaskr.views import login_required, admin_required


bp = Blueprint("rooms", __name__, url_prefix="/rooms")


def get_room_from_hash_id(hash_id):
    room_list = Room.query.filter_by(hash_id=hash_id).all()
    if len(room_list) == 0:
        return None
    return room_list[0]

def get_scenarios():
    scenario_list = Scenario.query.all()
    if len(scenario_list) == 0:
        return None
    return scenario_list

@socketio.on("join")
def on_join(payload):
    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if not user.is_admin():
        hash_id = payload["hash_id"]
        session["hash_id"] = hash_id
        join_room(hash_id)
        emit("room_message", {"name": user.name, "text": "入室しました"}, room=hash_id)

@socketio.on("disconnect")
def on_disconnect():
    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if not user.is_admin():
        hash_id = session.get("hash_id")
        emit("room_message", {"name": user.name, "text": "退室しました"}, room=hash_id)
        session.pop("hash_id", None)
        leave_room(hash_id)

@socketio.on("create_message")
def on_create_message(payload):
    hash_id = payload["hash_id"]
    text = payload["text"]

    user_id = session.get("user_id")
    room = get_room_from_hash_id(hash_id)
    message = Message(
            text=text,
            user_id=user_id,
            room_id=room.id,
            )
    db.session.add(message)
    db.session.commit()

    user = User.query.get(user_id)
    emit("room_message", {"name": user.name, "text": text}, room=hash_id)

@bp.route("/")
@login_required
def index():
    """
    [GET] /rooms

    ルームの一覧
    """

    if g.user.is_admin():
        rooms = Room.query.all()
    else:
        rooms = Room.query.filter_by(status=Status.AVAILABLE).all()
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

    try:
        if g.user.is_admin():
            scenarios = room.scenarios
            return render_template("rooms/show.html", room=room, scenarios=scenarios)

        room.join_user(g.user)
        scenario = room.fetch_scenario_of(g.user)
        return render_template("rooms/show.html", room=room, scenarios=[scenario])
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

    room = get_room_from_hash_id(hash_id)
    scenarios = get_scenarios()
    if room is None or scenarios is None:
        abort(404)

    if request.method == "POST":
        try:
            if "scenarios" in request.form:
                room.scenarios = []
                for scenario_id in request.form.getlist("scenarios"):
                    scenario_id = int(scenario_id)
                    scenario = Scenario.query.get(scenario_id)
                    room.scenarios.append(scenario)

            if "status" in request.form:
                room.status = request.form["status"]

            if "name" in request.form:
                room.name = request.form["name"]

            db.session.add(room)
            db.session.commit()

        except ValidationError as error:
            flash(error.args[0])
            return redirect(url_for("rooms.edit", hash_id=hash_id))

        return redirect(url_for("rooms.index"))

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
