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
    user_id = random.randint(1,100000)
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

