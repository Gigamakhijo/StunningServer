from fastapi.testclient import TestClient
import pytest
import sqlite3

from .main import app, get_password_hash
from . import db
from . import utils


client = TestClient(app)


@pytest.fixture
def cur():
    con = db.connect()
    yield con.cursor()
    con.close()


def login(username: str, password: str):
    response = client.post("/token", data={"username": username, "password": password})
    return response


def test_register_success(cur):
    email = utils.randomword(10)
    passwd = utils.randomword(10)

    response = client.post("/register", data={"username": email, "password": passwd})

    res = cur.execute("SELECT * FROM USERS WHERE email=?", (email,))
    row = res.fetchone()

    assert row["email"] == email, "이메일 틀림"
    assert response.status_code == 200
    assert response.json()["detail"] == "Signup Successful"

    response = client.post("/register", data={"username": email, "password": passwd})

    assert response.status_code == 409
    assert response.json()["detail"] == "User already exists"


def test_login_fail_no_user():
    # not in db
    response = login("asdlfkaj", "test")
    assert response.status_code == 401
    assert response.json() == {"msg": "Incorrect username or password"}


def test_login_fail_incorrect_passwd():
    # not in db
    response = login("test", "asdfasdf")
    assert response.status_code == 401
    assert response.json() == {"msg": "Incorrect username or password"}


def test_login_success():
    response = login("test", "test")
    assert response.status_code == 401
    assert response.json() == {"msg": "Incorrect username or password"}
