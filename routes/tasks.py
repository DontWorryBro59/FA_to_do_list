from typing import Annotated

from fastapi import Depends, APIRouter

from models.schemas import TaskSchema, MessageSchema, TaskSchemaForOrm, AssignIDTaskSchema
from repository import TaskRepository

tasks_router = APIRouter(prefix="/tasks",
                         tags=['🗒 Tasks / Задачи'])


@tasks_router.get('/get_tasks/',
                  summary='Get task list / Получить список задач')
async def get_tasks() -> list[TaskSchemaForOrm]:
    result = await TaskRepository.select_tasks()
    return result


@tasks_router.get('/get_tasks_without_executor/',
                  summary='Get tasks without executor / Получить задачи без исполнителя')
async def get_tasks_without_executor() -> list[TaskSchemaForOrm]:
    result = await TaskRepository.select_tasks_without_executor()
    return result


@tasks_router.get('/get_tasks_with_executor/',
                  summary='Get tasks with executor / Получить задачи с исполнителем')
async def get_tasks_with_executor() -> list[TaskSchemaForOrm]:
    result = await TaskRepository.select_tasks_with_executor()
    return result


@tasks_router.post('/add_task/',
                   summary='Add task / Добавить задачу')
async def add_task(task: Annotated[TaskSchema, Depends()]) -> MessageSchema:
    task_id = await TaskRepository.add_task(task)
    message = MessageSchema(message="Task added with id {}".format(task_id))
    return message


@tasks_router.put('/update_task/',
                   summary='Update task / Обновить задачу')
async def update_task(task: Annotated[TaskSchemaForOrm, Depends()]) -> MessageSchema:
    msg = await TaskRepository.change_task(task)
    message = MessageSchema(message=msg)
    return message


@tasks_router.patch('/assign_user_to_task_id/',
                   summary='Assign user to task / Присвоить пользователю задачу')
async def assign_user_to_task_id(data: Annotated[AssignIDTaskSchema, Depends()]) -> MessageSchema:
    msg = await TaskRepository.assign_task_for_id(data)
    message = MessageSchema(message=msg)
    return message


@tasks_router.delete('/delete_task_by_id/',
                     summary='Delete task by id / Удалить задачу по id')
async def delete_task_by_id(task_id: int) -> MessageSchema:
    msg = await TaskRepository.delete_task(task_id)
    message = MessageSchema(message=msg)
    return message
