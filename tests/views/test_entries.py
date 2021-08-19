import pytest
from flaskr.models import Entry


def test_index(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/entries", follow_redirects=True)
    assert 200 == response.status_code
    assert b"entry1" in response.data

def test_edit(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/entries/2/edit")
    assert 200 == response.status_code
    assert b"entry2" in response.data

    # [POST]
    response = client.post(
            "/entries/2/edit",
            data={"title": "updated", "text": "updated"},
            follow_redirects=True)
    assert 200 == response.status_code
    with app.app_context():
        entry = Entry.query.get(2)
        assert entry.title == "updated"

def test_create(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/entries/create")
    assert 200 == response.status_code

    # [POST]
    response = client.post(
            "/entries/create",
            data={"title": "a", "text": "a"}
            )
    assert "http://localhost/entries/" == response.headers["Location"]
    with app.app_context():
        entry_list = Entry.query.filter(Entry.title=="a").all()
        assert len(entry_list) is not 0

def test_delete(client, auth, app):
    # [POST]
    auth.login()
    response = client.post("/entries/2/delete")
    assert response.headers["Location"] == "http://localhost/entries/"

    with app.app_context():
        entry = Entry.query.get(2)
        assert entry is None
