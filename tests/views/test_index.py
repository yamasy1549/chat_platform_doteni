import pytest


def test_root(client, auth, app):
    # [GET]
    response = client.get("/")
    assert "http://localhost/entries/" == response.headers["Location"]
