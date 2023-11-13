from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from .. import db

router = APIRouter()


class User(BaseModel):
    username: str
    target_username: str


class Mate(BaseModel):
    first_username: str
    second_username: str


@router.get("/mate/search/{username}")
def searching_user(username: str):
    con = db.connect()
    cur = con.cursor()

    cur.execute("SELECT * FROM USERS WHERE username=?", (username,))
    user = cur.fetchone()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )

    return user


@router.post("/mate/follow")
def following_request(user: User):
    con = db.connect()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM FOLLOW_REQUEST WHERE username=? and target_username =?",
        (
            user.username,
            user.target_username,
        ),
    )

    res = cur.fetchone()

    if res is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Request already exists"
        )

    cur.execute(
        "INSERT INTO FOLLOW_REQUEST (username,target_username) VALUES(?,?)",
        (
            user.username,
            user.target_username,
        ),
    )
    con.commit()

    return HTTPException(status_code=status.HTTP_200_OK, detail="Request Success")

    ...


@router.post("/mate/follow/accept")
def accept_request(mate: Mate):
    # delete request , add mate
    con = db.connect()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM FOLLOW_REQUEST WHERE username =? and target_username =?",
        (
            mate.first_username,
            mate.second_username,
        ),
    )

    cur.execute(
        "INSERT INTO MATE(first_username,second_username) VALUES(?,?)",
        (
            mate.first_username,
            mate.second_username,
        ),
    )
    con.commit()
    ...


@router.post("/mate/follow/cancel")
def cancel_request(user: User):
    con = db.connect()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM FOLLOW_REQUEST WHERE username =? and target_username =?",
        (
            user.username,
            user.target_username,
        ),
    )
    con.commit()
    ...
