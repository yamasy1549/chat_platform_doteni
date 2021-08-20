import pytest
from flaskr.models.user import User


def test_index(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/users", follow_redirects=True)
    assert 200 == response.status_code
    assert b"test1" in response.data

def test_edit(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/users/2/edit")
    assert 200 == response.status_code
    assert b"test2" in response.data

    # [POST]
    response = client.post(
            "/users/2/edit",
            data={"name": "updated", "password": "updated"},
            follow_redirects=True)
    assert 200 == response.status_code
    with app.app_context():
        user = User.query.get(2)
        assert user.name == "updated"

def test_create(client, auth, app):
    # [GET]
    response = client.get("/users/create")
    assert 200 == response.status_code

    # [POST] ログイン前
    response = client.post(
            "/users/create",
            data={"name": "aaaaa", "password": "aaaaa"}
            )
    assert "http://localhost/" == response.headers["Location"]

    # [POST] ログイン後
    auth.login()
    response = client.post(
            "/users/create",
            data={"name": "bbbbb", "password": "bbbbb"}
            )
    assert "http://localhost/users/" == response.headers["Location"]

    with app.app_context():
        user_list = User.query.filter(User.name=="aaaaa").all()
        assert len(user_list) is not 0

def test_delete(client, auth, app):
    # [POST]
    auth.login()
    response = client.post("/users/2/delete")
    assert response.headers["Location"] == "http://localhost/users/"

    with app.app_context():
        user = User.query.get(2)
        assert user is None

@pytest.mark.parametrize(("name", "role", "password", "message"), (
    ("", 1, "", "ユーザ名は必須です。".encode()),
    ("test1", 1, "ccccc", "ユーザ名はすでに登録されています。".encode()),
    ("ccccc", 1, "c", "パスワードは3文字以上にしてください。".encode()),
    ("ccccc", 10000, "ccccc", "ロールの値を正しく指定してください。".encode()),
))
def test_register_validate_input(client, name, role, password, message):
    response = client.post(
        "/users/create",
        data={"name": name, "role": role, "password": password},
        follow_redirects=True
    )
    print(response.data.decode())
    assert message in response.data
