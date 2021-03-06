import pytest
from flaskr.models import Room, Status


def get_hash_id(app, id):
    with app.app_context():
        room = Room.query.get(id)
        return room.hash_id

def test_index(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/rooms", follow_redirects=True)
    assert 200 == response.status_code
    assert "ルーム新規登録".encode() in response.data

def test_show(client, auth, app):
    hash_id = get_hash_id(app, 3)

    # [GET] 1人目
    auth.login(name="test2", password="test2")
    response = client.get("/rooms/{}".format(hash_id))
    assert 200 == response.status_code
    assert "scenario1".encode() in response.data
    assert "scenario2".encode() not in response.data

    # [GET] 2人目
    auth.login(name="test3", password="test3")
    response = client.get("/rooms/{}".format(hash_id))
    assert 200 == response.status_code
    assert "scenario1".encode() not in response.data
    assert "scenario2".encode() in response.data

    # [GET] 3人目
    auth.login(name="test4", password="test4")
    response = client.get("/rooms/{}".format(hash_id))
    assert "ルームは満員です。".encode() not in response.data

def test_edit(client, auth, app):
    hash_id = get_hash_id(app, 2)

    # [GET]
    auth.login()
    response = client.get("/rooms/{}/edit".format(hash_id))
    assert 200 == response.status_code
    assert "ステータス".encode() in response.data

    # [POST]
    response = client.post(
            "/rooms/{}/edit".format(hash_id),
            data={"status": 4},
            follow_redirects=True)
    assert 200 == response.status_code
    with app.app_context():
        room = Room.query.get(2)
        assert room.status == Status(4)

def test_create(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/rooms/create")
    assert 200 == response.status_code

    # [POST]
    response = client.post(
            "/rooms/create",
            )
    assert "http://localhost/rooms/" == response.headers["Location"]
    with app.app_context():
        room_list = Room.query.filter_by(status=Status(1)).all()
        assert len(room_list) is not 0

def test_delete(client, auth, app):
    hash_id = get_hash_id(app, 2)

    # [POST]
    auth.login()
    response = client.post("/rooms/{}/delete".format(hash_id))
    assert response.headers["Location"] == "http://localhost/rooms/"

    with app.app_context():
        room = Room.query.get(2)
        assert room is None

@pytest.mark.parametrize(("status", "message"), (
    (10000, "ステータスの値を正しく指定してください。".encode()),
))
def test_register_validate_input(client, auth, status, message):
    auth.login()
    response = client.post(
        "/rooms/create",
        data={"status": status},
        follow_redirects=True
    )
    print(response.data.decode())
    assert message in response.data
