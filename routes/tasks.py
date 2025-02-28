from typing import Annotated

from fastapi import Depends, APIRouter

from models.schemas import TaskSchema, MessageSchema
from repository import TaskRepository

tasks_router = APIRouter(prefix="/tasks",
                         tags=['🗒 Tasks / Задачи'])


@tasks_router.get('/tasks/get_tasks/',
                  summary='Get task list / Получить список задач')
async def get_tasks() -> list[TaskSchema]:
    pass


@tasks_router.post('/tasks/add_task/',
                   summary='Add task / Добавить задачу')
async def add_task(task: Annotated[TaskSchema, Depends()]) -> MessageSchema:
    pass