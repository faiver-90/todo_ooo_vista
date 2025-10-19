from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ToDoBase(BaseModel):
    """
    Base schema for ToDo items.

    Contains shared fields used across create, read, and update operations.
    """

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None


class ToDoCreate(ToDoBase):
    """
    Schema for creating a new ToDo item.

    Inherits all base fields from ToDoBase.
    """

    pass


class ToDoUpdate(BaseModel):
    """
    Schema for updating an existing ToDo item.

    Allows partial updates and forbids extra fields.
    """

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    is_completed: bool | None = None

    model_config = ConfigDict(extra="forbid")


class ToDoRead(ToDoBase):
    """
    Schema for reading ToDo items from the database.

    Includes read-only fields such as IDs and timestamps.
    """

    id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ToDoListResponse(BaseModel):
    """
    Schema for representing a paginated list of ToDo items.
    """

    items: list[ToDoRead]


class MessageResponse(BaseModel):
    """
    Simple message response schema for API operations.
    """

    message: str
