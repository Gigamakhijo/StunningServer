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
    ...


def test_register_success(cur):
    email = utils.randomword(10)
    passwd = utils.randomword(10)

    response = client.post(
        "/auth/register", data={"username": email, "password": passwd}
    )

    res = cur.execute("SELECT * FROM USERS WHERE email=?", (email,))
    row = res.fetchone()

    assert row["email"] == email, "이메일 틀림"
    assert response.status_code == 200
    assert response.json()["detail"] == "Signup Successful"

    response = client.post(
        "/auth/register", data={"username": email, "password": passwd}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "User aslready exists"


def test_login_success():
    email = utils.randomword(10)
    passwd = utils.randomword(10)
    response = client.post(
        "/auth/register", data={"username": email, "password": passwd}
    )

    assert response.status_code == 200, "가입 잘못됐음"

    response = client.post("/auth/token", data={"username": email, "password": passwd})
    json = response.json()

    assert response.status_code == 200

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"{json['token_type']} {json['access_token']}",
        },
    )
    assert response.status_code == 200


def test_login_fail_no_user(cur):
    # not in db
    passwd = utils.randomword(10)

    user = "asdfasd"
    while user is not None:
        email = utils.randomword(10)
        user = db.get_user(email)

    response = client.post("/auth/token", data={"username": email, "password": passwd})

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_fail_incorrect_passwd():
    # not in db
    email = "sdvddsas"
    passwd = "asddddaff"

    response = client.post(
        "/auth/register", data={"username": email, "password": passwd}
    )

    assert response.status_code == 200

    response = client.post("/auth/token", data={"username": email, "password": "tfdht"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
