from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.schemas import Status


class Base(DeclarativeBase):
    pass


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_worker_name: Mapped[str] = mapped_column(String(200), nullable=False)
    worker_post: Mapped[str] = mapped_column(String(200), nullable=False)
    # hashed_password: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)


class TasksORM(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    status: Mapped[Status] = mapped_column(nullable=False, default=Status.TODO)
    executor: Mapped[str] = mapped_column(String(100), nullable=True)
    date_of_creation: Mapped[datetime] = mapped_column(default=datetime.now())
    date_of_completion: Mapped[datetime | None] = mapped_column(default=None)
