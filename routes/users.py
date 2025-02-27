from typing import Annotated

from fastapi import APIRouter, Depends

from fake_db import users as fake_db_user
from schemas import UserSchema

users_router = APIRouter(prefix='/users')


@users_router.get('/get_users/')
async def get_users():
    users = fake_db_user
    return {"message": fake_db_user.users}


@users_router.post('/add_user/')
async def add_user(user: Annotated[UserSchema, Depends()]) -> dict:
    fake_db_user.append(user)
    return {"message": "User added"}
