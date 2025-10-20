from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db.base import Base


class ToDo(Base):
    """
    SQLAlchemy ORM model representing a ToDo entity.

    Defines the schema for the 'todos' table, which stores information about
    individual tasks, their completion status, and timestamps.

    Attributes:
        id (int): Primary key, unique identifier of the ToDo item.
        title (str): Title of the task.
        description (str | None): Optional detailed description.
        is_completed (bool): Indicates whether the task is completed.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last updated.
        is_deleted (bool): Soft delete flag.
    """

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
