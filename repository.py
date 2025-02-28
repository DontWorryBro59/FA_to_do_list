from sqlalchemy import select

from database import new_session
from models.orm_model import UsersORM, TasksORM
from models.schemas import UserSchema, TaskSchema, UserSchemaForORM, TaskSchemaForOrm


class UserRepository:
    @classmethod
    async def add_user(cls, data: UserSchema) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()
            user = UsersORM(**user_dict)
            session.add(user)
            print('[LOG] User was added')
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


class TaskRepository:
    @classmethod
    async def add_task(cls, data: TaskSchema) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TasksORM(**task_dict)
            session.add(task)
            print('[LOG] Task was added')
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
            try:
                old_task.task_name = data.task_name
                old_task.description = data.description
                old_task.date_of_creation = data.date_of_creation
                old_task.date_of_completion = data.date_of_completion
                await session.commit()
            except Exception as e:
                return str(e)
        return f'Запись с id {task_id} была изменена'
