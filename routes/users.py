from typing import Annotated

from fastapi import APIRouter, Depends

from fake_db import users as fake_db_user
from models.schemas import UserSchema

users_router = APIRouter(prefix='/users',
                         tags=['👨‍🔧 Users / Пользователи'])


@users_router.get('/get_users/',
                  summary='Get user list / Получить список пользователей')
async def get_users():
    users = fake_db_user
    return {"message": fake_db_user.users}


@users_router.post('/add_user/',
                   summary='Add user / Добавить пользователя')
async def add_user(user: Annotated[UserSchema, Depends()]) -> dict:
    fake_db_user.append(user)
    return {"message": "User added"}
