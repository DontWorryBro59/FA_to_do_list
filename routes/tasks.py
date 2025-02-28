from typing import Annotated

from fastapi import Depends, APIRouter

from models.schemas import TaskSchema, MessageSchema, TaskSchemaForOrm
from repository import TaskRepository

tasks_router = APIRouter(prefix="/tasks",
                         tags=['🗒 Tasks / Задачи'])


@tasks_router.get('/tasks/get_tasks/',
                  summary='Get task list / Получить список задач')
async def get_tasks() -> list[TaskSchemaForOrm]:
    result = await TaskRepository.select_tasks()
    return result


@tasks_router.post('/tasks/add_task/',
                   summary='Add task / Добавить задачу')
async def add_task(task: Annotated[TaskSchema, Depends()]) -> MessageSchema:
    task_id = await TaskRepository.add_task(task)
    message = MessageSchema(message="Task added with id {}".format(task_id))
    return message

@tasks_router.post('/tasks/update_task/',
                   summary='Update task / Обновить задачу')
async def update_task(task: Annotated[TaskSchemaForOrm, Depends()]) -> MessageSchema:
    msg = await TaskRepository.change_task(task)
    message = MessageSchema(message=msg)
    return message
