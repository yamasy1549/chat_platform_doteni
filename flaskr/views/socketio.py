from flask import current_app, session
from flask_socketio import emit, join_room, leave_room
from flaskr.core import db, socketio
from flaskr.models import Message
from flaskr.views.rooms import fetch_user, fetch_room_from_hash_id


clients = set()


def send_room_message(user, hash_id, text, save=True, classname=""):
    room = fetch_room_from_hash_id(hash_id)
    scenario = room.fetch_scenario_of(user)

    emit("room_message", {"name": scenario.displayname_of(user), "text": text, "classname": classname}, room=hash_id)

    if save:
        message = Message(
                text=text,
                user_id=user.id,
                room_id=room.id,
                )

        db.session.add(message)
        db.session.commit()

        current_app.logger.info(f"[/rooms/{hash_id}] {user} {message}")


@socketio.on("join")
def on_join(payload):
    """
    [socketio] join

    入室時のイベント
    """

    user = fetch_user()

    if not user.is_admin():
        hash_id = payload["hash_id"]
        session["hash_id"] = hash_id

        join_room(hash_id)
        #  send_room_message(user, hash_id, "### 入室しました ###", save=False, classname="log")

        clients.add(user.name)
        emit("room_user", {"users": list(clients)}, room=hash_id)

@socketio.on("disconnect")
def on_disconnect():
    """
    [socketio] disconnect

    退室時のイベント
    """

    user = fetch_user()

    if not user.is_admin():
        hash_id = session.get("hash_id")
        session.pop("hash_id", None)

        #  send_room_message(user, hash_id, "### 退室しました ###", save=False, classname="log")
        leave_room(hash_id)

        clients.discard(user.name)
        emit("room_user", {"users": list(clients)}, room=hash_id)

@socketio.on("meta_start_message")
def on_meta_start_message():
    """
    [socketio] meta_start_message

    対話開始時のイベント
    """

    user = fetch_user()

    if not user.is_admin():
        hash_id = session.get("hash_id")

        send_room_message(user, hash_id, "### 対話開始 ###", classname="log")

@socketio.on("meta_end_message")
def on_meta_end_message():
    """
    [socketio] meta_end_message

    対話終了時のイベント
    """

    user = fetch_user()

    if not user.is_admin():
        hash_id = session.get("hash_id")

        send_room_message(user, hash_id, "### 対話終了 ###", classname="log")


@socketio.on("create_message")
def on_create_message(payload):
    """
    [socketio] create_message

    メッセージ送信時のイベント
    """

    user = fetch_user()

    if not user.is_admin():
        hash_id = payload["hash_id"]
        text = payload["text"]

        send_room_message(user, hash_id, text)
