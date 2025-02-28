from typing import Annotated

from fastapi import APIRouter, Depends

from models.schemas import UserSchemaForORM, UserSchema, MessageSchema
from repository import UserRepository

users_router = APIRouter(prefix='/users',
                         tags=['👨‍🔧 Users / Пользователи'])


@users_router.get('/get_users/',
                  summary='Get user list / Получить список пользователей')
async def get_users() -> list[UserSchemaForORM]:
    users = await UserRepository.select_users()
    return users


@users_router.post('/add_user/',
                   summary='Add user / Добавить пользователя')
async def add_user(user: Annotated[UserSchema, Depends()]) -> MessageSchema:
    user_id = await UserRepository.add_user(user)
    message = MessageSchema(message="User added with id {}".format(user_id))
    return message
