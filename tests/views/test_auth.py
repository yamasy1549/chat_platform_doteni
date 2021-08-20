import pytest
from flask import session


def test_login(client, auth, app):
    assert client.get("/auth/login").status_code == 200

    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/")
        assert session["user_id"] == 1

@pytest.mark.parametrize(("name", "password", "message"), (
    ("a", "test", "ユーザ名かパスワードが違います。".encode()),
    ("test", "a", "ユーザ名かパスワードが違います。".encode()),
))
def test_login_validate_input(auth, name, password, message):
    response = auth.login(name, password)
    assert message in response.data

def test_logout(client, auth, app):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
