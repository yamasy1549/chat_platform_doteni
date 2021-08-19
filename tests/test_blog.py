import pytest
from flaskr.db import get_db


def test_index(client, auth):
    auth.login()
    response = client.get("/blog/")
    assert "ログアウト".encode() in response.data
    assert b"test title" in response.data
    assert b"test (2018-01-01)" in response.data
    assert b"test\nbody" in response.data
    assert b'href="/blog/1/update"' in response.data

@pytest.mark.parametrize(("path", "method"), (
    ("/blog/", "GET"),
    ("/blog/create", "GET"),
    ("/blog/create", "POST"),
    ("/blog/1/update", "GET"),
    ("/blog/1/update", "POST"),
    ("/blog/1/delete", "POST"),
))
def test_login_required_post(client, path, method):
    if method == "GET":
        response = client.get(path)

    if method == "POST":
        response = client.post(path)

    assert response.headers["Location"] == "http://localhost/auth/login"


def test_author_required(app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE post SET author_id = 2 WHERE id = 1")
        db.commit()

    auth.login()
    assert client.post("/blog/1/update").status_code == 403
    assert client.post("/blog/1/delete").status_code == 403
    assert b'href="/1/update"' not in client.get("/blog/").data


@pytest.mark.parametrize("path", (
    "/blog/2/update",
    "/blog/2/delete",
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

def test_create(client, auth, app):
    auth.login()
    assert client.get("/blog/create").status_code == 200
    client.post("/blog/create", data={"title": "created", "body": ""})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM post").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/blog/1/update").status_code == 200
    client.post("/blog/1/update", data={"title": "updated", "body": ""})

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post["title"] == "updated"


@pytest.mark.parametrize("path", (
    "/blog/create",
    "/blog/1/update",
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    assert "タイトルが必須です。".encode() in response.data

def test_delete(client, auth, app):
    auth.login()
    response = client.post("/blog/1/delete")
    assert response.headers["Location"] == "http://localhost/blog/"

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM post WHERE id = 1").fetchone()
        assert post is None
