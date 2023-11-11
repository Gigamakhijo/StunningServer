from fastapi.testclient import TestClient
import os
import sqlite3

from .main import app


client = TestClient(app)


def login(username: str, password: str):
    response = client.post("/token", data={"username": username, "password": password})
    return response


def signup(email: str, password: str):
    response = client.post("/register", data={"username": email, "password": password})
    return response


def test_register_success():
    email = "leewoorim@test.com"
    passwd = "leewoorim"

    con = sqlite3.connect(path, check_same_thread=False)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.commit()

    response = signup(email=email, password=passwd)

    cur.execute("SELECT * FROM USERS WHERE email=?", (email,))

    res = cur.fetchone()

    assert res is not None
    assert res["email"] == email
    print(res)
    assert response.status_code == 200
    assert response.json() == {"detail": "Signup Successful"}


def test_register_fail():
    email = "test@test.com"
    passwd = "test"

    response = signup(email=email, password=passwd)

    con = sqlite3.connect(path, check_same_thread=False)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM USERS WHERE email=?", (email,))

    db = cur.fetchone()

    assert response.status_code == 200
    assert response.json() == {"msg": "Signup Successful"}


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
