from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends, APIRouter
from app.routers.auth import get_current_user


class User(BaseModel):
    email: str


router = APIRouter()


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    return current_user
