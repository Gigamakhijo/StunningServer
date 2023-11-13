import pytest
from fastapi.testclient import TestClient

from . import db, utils
from .main import app

client = TestClient(app)


@pytest.fixture
def cur():
    con = db.connect()
    yield con.cursor()
    con.close()


# 검색 시 유저있을때
def test_search_result_success():
    username = "leewoorim"

    res = client.get(f"/mate/search/{username}")

    user = res.json()
    assert res.status_code == 200, res.text
    assert user["username"] == username, "유저네임 틀렸음"

    ...


# 검색 시 유저가없을때
def test_search_result_failed():
    username = "asdfghjkl"

    res = client.get(f"/mate/search/{username}")
    assert res.status_code == 404, res.text
    ...


# 요청 중복이 아닐 때 팔로우
def test_request_confirm_success(cur):
    username = utils.randomword(10)
    target_username = utils.randomword(10)

    body = {"username": username, "target_username": target_username}

    res = client.post(
        "/mate/follow",
        json=body,
    )

    assert res.status_code == 200

    res = cur.execute(
        "SELECT * FROM FOLLOW_REQUEST WHERE username=? and target_username =?",
        (
            username,
            target_username,
        ),
    )

    res = res.fetchone()
    assert res["username"] == username, "username error"
    assert res["target_username"] == target_username, "target_username error"

    ...


# 요청이 중복일떄 팔로우
def test_request_confirm_failed():
    username = "leewoorim"
    target_username = "ohsujin"

    body = {"username": username, "target_username": target_username}

    res = client.post("/mate/follow", json=body)

    assert res.status_code == 409

    ...


# 요청 수락 했을 떄
def test_request_accept():
    first_username = utils.randomword(10)
    second_username = utils.randomword(10)

    con = db.connect()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO FOLLOW_REQUEST (username,target_username) VALUES(?,?)",
        (
            first_username,
            second_username,
        ),
    )
    con.commit()

    body = {"first_username": first_username, "second_username": second_username}

    res = client.post("/mate/follow/accept", json=body)

    assert res.status_code == 200

    res = cur.execute(
        "SELECT * FROM MATE WHERE first_username =? and second_username = ?",
        (
            first_username,
            second_username,
        ),
    )

    res = cur.fetchone()
    assert res["first_username"] == first_username, "first username error"
    assert res["second_username"] == second_username, "second username error"

    ...


# 요청 취소했을 때
def test_request_cancel(printer):
    username = utils.randomword(10)
    target_username = utils.randomword(10)

    con = db.connect()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO FOLLOW_REQUEST(username,target_username) VALUES (?,?)",
        (
            username,
            target_username,
        ),
    )
    con.commit()

    body = {"username": username, "target_username": target_username}
    client.post("/mate/follow/cancel", json=body)

    res = cur.execute(
        "SELECT * FROM FOLLOW_REQUEST WHERE username =? and target_username = ?",
        (
            username,
            target_username,
        ),
    )
    res = res.fetchone()
    assert res is None, "요청 취소 실패"
    ...
