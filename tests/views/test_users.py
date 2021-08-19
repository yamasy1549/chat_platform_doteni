import pytest
from flaskr.models import User


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
            data={"name": "updated", "email": "updated", "password": "updated"},
            follow_redirects=True)
    assert 200 == response.status_code
    with app.app_context():
        user = User.query.get(2)
        assert user.name == "updated"

def test_create(client, auth, app):
    # [GET]
    response = client.get("/users/create")
    assert 200 == response.status_code

    # [POST]
    response = client.post(
            "/users/create",
            data={"name": "a", "email": "a", "password": "a"}
            )
    assert "http://localhost/auth/login" == response.headers["Location"]
    with app.app_context():
        user_list = User.query.filter(User.name=="a").all()
        assert len(user_list) is not 0

def test_delete(client, auth, app):
    # [POST]
    auth.login()
    response = client.post("/users/2/delete")
    assert response.headers["Location"] == "http://localhost/users/"

    with app.app_context():
        user = User.query.get(2)
        assert user is None

@pytest.mark.parametrize(("name", "email", "password", "message"), (
    ("", "", "", "名前を入力してください。".encode()),
    ("a", "", "", "メールアドレスを入力してください。".encode()),
    ("a", "test1", "", "パスワードを入力してください。".encode()),
    ("a", "test1", "a", "メールアドレスはすでに登録されています。".encode()),
))
def test_register_validate_input(client, name, email, password, message):
    response = client.post(
        "/users/create",
        data={"name": name, "email": email, "password": password},
        follow_redirects=True
    )
    print(response.data.decode())
    assert message in response.data
