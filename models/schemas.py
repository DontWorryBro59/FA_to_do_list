from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, ConfigDict, AfterValidator


# Schemas for TASKS =====================================================================================
def check_data_of_completion(user_date: datetime) -> datetime:
    if user_date <= datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Date of completion must be greater than date of creation")
    return user_date


def check_data_of_creation(user_date: datetime) -> datetime:
    if user_date >= datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Date of completion must be greater than date of creation")
    return user_date


class Status(str, Enum):
    DONE = "DONE"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"


class TaskSchema(BaseModel):
    task_name: str = Field(..., min_length=5, max_length=100, description="Task name / Название задачи")
    description: str = Field(..., min_length=5, max_length=300, description="Task description / Описание задачи")
    status: Status = Field(default=Status.TODO, description="Task status (DONE, TODO, IN_PROGRESS) / Статус задачи")
    executor: str | None = Field(default=None, description='Task executor / Ответственный за выполнение задачи')
    # date_of_creation: datetime = Field(default=datetime.now(), description='Task creation date / Дата создания задачи')
    # date_of_completion: datetime | None = Field(default=None, description='Task completion date / Дата завершения задачи')
    date_of_creation: datetime = Field(
        default=datetime.now(),
        description='Task creation date / Дата создания задачи')
    date_of_completion: Annotated[datetime, AfterValidator(check_data_of_completion)] = Field(
        default=datetime.now() + timedelta(days=1),
        description="Task completion date / Дата завершения задачи")


class TaskSchemaForOrm(TaskSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AssignIDTaskSchema(BaseModel):
    task_id: int = Field(..., description="Task ID / ID задачи")
    user_id : int = Field(..., description="User ID / ID пользователя")


# Schemas for Users =====================================================================================
class UserSchema(BaseModel):
    full_worker_name: str = Field(..., min_lenght=2, max_length=100, description="User name / Имя пользователя")
    worker_post: str = Field(..., min_length=2, max_length=100, description="Worker post / Почта работника")


class UserSchemaForORM(UserSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MessageSchema(BaseModel):
    message: str = Field(default='Some message about Response', min_length=5, max_length=100,
                         description="Message / Сообщение")
