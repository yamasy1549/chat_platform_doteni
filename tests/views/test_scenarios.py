import pytest
from flaskr.models import Scenario


def test_index(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/scenarios", follow_redirects=True)
    assert 200 == response.status_code
    assert b"scenario1" in response.data

def test_edit(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/scenarios/2/edit")
    assert 200 == response.status_code
    assert b"scenario2" in response.data

    # [POST]
    response = client.post(
            "/scenarios/2/edit",
            data={"title": "updated", "text": "updated"},
            follow_redirects=True)
    assert 200 == response.status_code
    with app.app_context():
        scenario = Scenario.query.get(2)
        assert scenario.title == "updated"

def test_create(client, auth, app):
    # [GET]
    auth.login()
    response = client.get("/scenarios/create")
    assert 200 == response.status_code

    # [POST]
    response = client.post(
            "/scenarios/create",
            data={"title": "a", "text": "a"}
            )
    assert "http://localhost/scenarios/" == response.headers["Location"]
    with app.app_context():
        scenario_list = Scenario.query.filter(Scenario.title=="a").all()
        assert len(scenario_list) is not 0

def test_delete(client, auth, app):
    # [POST]
    auth.login()
    response = client.post("/scenarios/2/delete")
    assert response.headers["Location"] == "http://localhost/scenarios/"

    with app.app_context():
        scenario = Scenario.query.get(2)
        assert scenario is None
