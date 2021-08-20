import pytest
from urllib.parse import urlencode

@pytest.mark.parametrize(("path", "method"), (
    ("/entries", "GET"), # TODO: なぜか /entries/ にリダイレクトされている？
))
def test_login_required(client, auth, path, method):
    if method == "GET":
        response = client.get(path)

    assert "http://localhost/auth/login?{}".format(urlencode({"next": path})) == response.headers["Location"]

@pytest.mark.parametrize(("path", "method"), (
    ("/entries/2/edit", "GET"),
    ("/entries/create", "GET"),
    ("/entries/2/delete", "POST"),
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
