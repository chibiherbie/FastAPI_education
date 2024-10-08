from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[int] = mapped_column(String(200), unique=True)
    username: Mapped[str] = mapped_column(String(200))
    name: Mapped[str] = mapped_column(String(200))
    hashed_password: Mapped[str] = mapped_column(String(200))
