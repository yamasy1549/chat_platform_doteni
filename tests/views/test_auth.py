import pytest
from flask import session


def test_login(client, auth, app):
    assert client.get("/auth/login").status_code == 200

    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/")
        assert session["user_id"] == 1

@pytest.mark.parametrize(("email", "password", "message"), (
    ("a", "test", "メールアドレスかパスワードが違います。".encode()),
    ("test", "a", "メールアドレスかパスワードが違います。".encode()),
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data

def test_logout(client, auth, app):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
