import pytest

@pytest.mark.parametrize("path", (
    "/entries",
    "/entries/2/edit",
    "/entries/create",
    "/entries/2/delete",
    "/users",
    "/users/2/edit",
    "/users/2/delete",
))
def test_login_required(client, path):
    response = client.post(path)
    assert "http://localhost/auth/login/" == response.headers["Location"]
