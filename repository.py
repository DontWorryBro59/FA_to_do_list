from fastapi import HTTPException, status as http_status
from sqlalchemy import select, delete

from database import new_session
from models.orm_model import UsersORM, TasksORM
from models.schemas import UserSchema, TaskSchema, UserSchemaForORM, TaskSchemaForOrm, AssignIDTaskSchema


class UserRepository:
    @classmethod
    async def add_user(cls, data: UserSchema) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()
            user = UsersORM(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def select_users(cls) -> list[UserSchemaForORM]:
        async with new_session() as session:
            query = select(UsersORM)
            result = await session.execute(query)
            orm_models = result.scalars().all()
            user_schemas = [UserSchemaForORM.model_validate(orm_model) for orm_model in orm_models]
            return user_schemas

    @classmethod
    async def delete_user(cls, id_user_to_delete: int) -> str:
        async with new_session() as session:
            check_user = select(UsersORM).where(UsersORM.id == id_user_to_delete)
            user = await session.execute(check_user)
            if not user.scalars().first():
                return f'Пользователь с id {id_user_to_delete} не был найден'
            query = delete(UsersORM).where(UsersORM.id == id_user_to_delete)
            try:
                await session.execute(query)
                await session.commit()
            except Exception as e:
                raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail=str(e))
        return f'Запись с id {id_user_to_delete} была удалена'

    @classmethod
    async def change_user(cls, data: UserSchemaForORM) -> str:
        print(data)
        async with new_session() as session:
            user_id = data.id
            query = select(UsersORM).where(UsersORM.id == user_id)
            old_user = await session.execute(query)
            old_user = old_user.scalars().first()
            if not old_user:
                return f'Запись с id {user_id} не была найдена'
            try:
                old_user.full_worker_name = data.full_worker_name
                old_user.worker_post = data.worker_post
                await session.commit()
            except Exception as e:
                raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail=str(e))
        return f'Запись с id {user_id} была изменена'


class TaskRepository:
    @classmethod
    async def add_task(cls, data: TaskSchema) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TasksORM(**task_dict)
            if await TaskRepository.check_user(task.executor):
                session.add(task)
                await session.flush()
                await session.commit()
                return task.id

    @classmethod
    async def select_tasks(cls) -> list[TaskSchemaForOrm]:
        async with new_session() as session:
            query = select(TasksORM)
            result = await session.execute(query)
            orm_models = result.scalars().all()
            task_schemas = [TaskSchemaForOrm.model_validate(orm_model) for orm_model in orm_models]
            return task_schemas

    @classmethod
    async def change_task(cls, data: TaskSchemaForOrm) -> str:
        async with new_session() as session:
            task_id = data.id
            query = select(TasksORM).where(TasksORM.id == task_id)
            old_task = await session.execute(query)
            old_task = old_task.scalars().first()
            if not old_task:
                return f'Запись с id {task_id} не была найдена'
            if not await TaskRepository.check_user(data.executor):
                return f'Исполнитель с таким именем не найден в списке пользователей'
            try:
                old_task.task_name = data.task_name
                old_task.description = data.description
                old_task.executor = data.executor
                old_task.date_of_creation = data.date_of_creation
                old_task.date_of_completion = data.date_of_completion
                await session.commit()
            except Exception as e:
                raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail=str(e))
        return f'Запись с id {task_id} была изменена'

    @classmethod
    async def assign_task_for_id(cls, data: AssignIDTaskSchema) -> str:
        async with new_session() as session:
            query = select(TasksORM).where(TasksORM.id == data.task_id)
            task = await session.execute(query)
            task = task.scalars().first()
            if not task:
                return f'Задача с id {data.task_id} не была найдена'
            query = select(UsersORM).where(UsersORM.id == data.user_id)
            user = await session.execute(query)
            user = user.scalars().first()
            if not user:
                return f'Пользователь с id {data.user_id} не был найден'
            try:
                task.executor = user.full_worker_name
                await session.commit()
            except Exception as e:
                raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail=str(e))
        return f'Запись с id {data.task_id} была изменена'

    @classmethod
    async def delete_task(cls, id_task_to_delete: int) -> str:
        async with new_session() as session:
            query = delete(TasksORM).where(TasksORM.id == id_task_to_delete)
            check_task = select(TasksORM).where(TasksORM.id == id_task_to_delete)
            check_result = await session.execute(check_task)
            if not check_result.scalars().first():
                return f'Задача с id {id_task_to_delete} не найдена'
            try:
                await session.execute(query)
                await session.commit()
            except Exception as e:
                raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail=str(e))
            return f'Запись с id {id_task_to_delete} была удалена'

    @classmethod
    async def select_tasks_without_executor(cls) -> list[TaskSchemaForOrm]:
        async with new_session() as session:
            query = select(TasksORM).where(TasksORM.executor == None)
            result = await session.execute(query)
            orm_models = result.scalars().all()
            task_schemas = [TaskSchemaForOrm.model_validate(orm_model) for orm_model in orm_models]
            return task_schemas

    @classmethod
    async def select_tasks_with_executor(cls) -> list[TaskSchemaForOrm]:
        async with new_session() as session:
            query = select(TasksORM).where(TasksORM.executor != None)
            result = await session.execute(query)
            orm_models = result.scalars().all()
            task_schemas = [TaskSchemaForOrm.model_validate(orm_model) for orm_model in orm_models]
            return task_schemas

    @staticmethod
    async def check_user(username: str) -> bool:
        async with new_session() as session:
            if not username:
                return True
            query = select(UsersORM).where(UsersORM.full_worker_name == username)
            user = await session.execute(query)
            user = user.scalars().all()
            if len(user) > 1:
                raise HTTPException(status_code=http_status.HTTP_409_CONFLICT,
                                    detail='Найдено больше одного пользователя с таким именем')
            elif len(user) == 1:
                return True
            else:
                raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail='Пользователь не найден')
