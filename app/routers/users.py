from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.routers.auth import get_current_user


class User(BaseModel):
    email: str


router = APIRouter()


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[
        User, Depends(get_current_user)
    ],  # depends: get_current_user가 있어야 api 사용가능을 의미
) -> User:
    return current_user
