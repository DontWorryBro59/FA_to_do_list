from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    worker_post: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
    # hashed_password: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
