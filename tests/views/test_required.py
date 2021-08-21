import pytest
from urllib.parse import urlencode

@pytest.mark.parametrize(("path", "method"), (
    ("/rooms", "GET"), # TODO: なぜか /rooms/ にリダイレクトされている？
    ("/rooms/1", "GET")
))
def test_login_required(client, auth, path, method):
    if method == "GET":
        response = client.get(path)

    assert "http://localhost/auth/login?{}".format(urlencode({"next": path})) == response.headers["Location"]

@pytest.mark.parametrize(("path", "method"), (
    ("/rooms/2/edit", "GET"),
    ("/rooms/create", "GET"),
    ("/rooms/2/delete", "POST"),
    ("/users", "GET"), # TODO: なぜか /users/ にリダイレクトされている？
    ("/users/2/edit", "GET"),
    ("/users/2/delete", "POST"),
))
def test_admin_required(client, auth, path, method):
    auth.login(name="test2", password="test2")

    if method == "GET":
        response = client.get(path)

    if method == "POST":
        response = client.post(path)

    assert "http://localhost/" == response.headers["Location"]
