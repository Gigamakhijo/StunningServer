from fastapi import APIRouter, HTTPException, status, Form
from typing import Annotated
from .. import db
from pydantic import BaseModel
import random

router = APIRouter()


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


class User(BaseModel):
    username: str
    target_username: str


@router.post("/mate/follow")
def following_request(
    username: Annotated[str, Form()], target_username: Annotated[str, Form()]
):
    con = db.connect()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM FOLLOW_REQUEST WHERE username=? and target_username =?",
        (
            username,
            target_username,
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
            username,
            target_username,
        ),
    )
    con.commit()

    return HTTPException(status_code=status.HTTP_200_OK, detail="Request Success")

    ...
