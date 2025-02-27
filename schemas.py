from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime

class Status(str, Enum):
    DONE = "DONE"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"

class TaskSchema(BaseModel):
    name: str = Field(..., min_length=5, max_length=50, description="Task name / Название задачи")
    description: str = Field(..., min_length=5, max_length=300, description="Task description / Описание задачи")
    status: Status = Field(default=Status.TODO, description="Task status (DONE, TODO, IN_PROGRESS) / Статус задачи")
    executor: str = Field (default=None, description='Task executor / Ответственный за выполнение задачи')
    date_of_creation: datetime = Field(..., description='Task creation date / Дата создания задачи')
    date_of_completion: datetime = Field(..., description='Task completion date / Дата завершения задачи')



class UserSchema(BaseModel):
    full_worker_name: str = Field(..., min_lenght=2, max_length=50, description="User name / Имя пользователя")
    worker_post: str = Field(..., min_length=2, max_length=50, description="Worker post / Почта работника")


