import random
import sqlite3

import pytest

from . import db, utils


def test_connect():
    con = db.connect()
    assert isinstance(con, sqlite3.Connection)


@pytest.fixture
def con():
    con = db.connect()
    yield con
    con.close()


def test_add_user(con):
    email = utils.randomword(10)
    hash = utils.randomword(10)
    user_id = 6000
    username = "leewoorim"
    state_comment = "asdfgd"

    db.add_user(user_id, email, hash, username, state_comment)

    cur = con.cursor()
    res = cur.execute("SELECT * FROM USERS WHERE email=?", (email,))
    user = res.fetchone()

    assert user is not None, "없는 유저"
    assert user["id"] == user_id, "user_id 틀림"
    assert user["email"] == email, "이메일 틀렸음"
    assert user["username"] == username, "유저네임 틀렸음"
    assert user["hashed_password"] == hash, "비밀번호 해시값 틀렸음"
    assert user["state_comment"] == state_comment, "상태메세지 틀림"


def test_get_user():
    email = utils.randomword(10)
    hash = utils.randomword(10)
    user_id = random.randint(1, 100000)
    username = "leewoorim"
    state_comment = "asdfgd"

    db.add_user(user_id, email, hash, username, state_comment)

    user = db.get_user(email)

    assert user is not None, "없는 유저"
    assert user["id"] == user_id, "user_id 틀림"
    assert user["email"] == email, "이메일 틀렸음"
    assert user["username"] == username, "유저네임 틀렸음"
    assert user["hashed_password"] == hash, "비밀번호 해시값 틀렸음"
    assert user["state_comment"] == state_comment, "상태메세지 틀림"


def test_add_request(con):
    request_id = random.randint(1, 100000)
    username = "leewoorim"
    target_username = "ohsujin"

    db.add_request(request_id, username, target_username)

    cur = con.cursor()
    res = cur.execute("SELECT * FROM FOLLOW_REQUEST WHERE id=?", (request_id,))
    res = res.fetchone()

    assert res is not None, "요청 실패"
    assert res["id"] == request_id, "request_id error"
    assert res["username"] == username, "요청 username error"
    assert res["target_username"] == target_username, "target_username error"
    ...


def test_get_request(con):
    request_id = random.randint(1, 1000)
    username = "leewoorim"
    target_username = "ohsujin"

    print(request_id)

    db.add_request(request_id, username, target_username)

    res = db.get_request(username, target_username)

    assert res is not None, "요청 확인 실패"
    assert res["username"] == username, "username error"
    assert res["target_username"] == target_username, "target_username error"
    ...
