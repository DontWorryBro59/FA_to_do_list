from typing import Annotated

from fastapi import Depends, APIRouter

from models.schemas import TaskSchema, MessageSchema
from repository import TaskRepository

tasks_router = APIRouter(prefix="/tasks",
                         tags=['🗒 Tasks / Задачи'])


@tasks_router.get('/tasks/get_tasks/',
                  summary='Get task list / Получить список задач')
async def get_tasks() -> list[TaskSchema]:
    result = await TaskRepository.select_tasks()
    return result


@tasks_router.post('/tasks/add_task/',
                   summary='Add task / Добавить задачу')
async def add_task(task: Annotated[TaskSchema, Depends()]) -> MessageSchema:
    task_id = await TaskRepository.add_task(task)
    message = MessageSchema(message="Task added with id {}".format(task_id))
    return message