from typing import Annotated

from fastapi import Depends, APIRouter

from fake_db import tasks as fake_db_task
from schemas import TaskSchema

tasks_router = APIRouter(prefix="/tasks")


@tasks_router.get('/tasks/get_tasks/')
async def get_tasks() -> list[TaskSchema]:
    return fake_db_task.tasks


@tasks_router.post('/tasks/add_task/')
async def add_task(task: Annotated[TaskSchema, Depends()]) -> dict:
    fake_db_task.append(task)
    return {"message": "Task added"}
