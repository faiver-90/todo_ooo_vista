from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ToDoBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None


class ToDoCreate(ToDoBase):
    pass


class ToDoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    is_completed: bool | None = None

    model_config = ConfigDict(extra="forbid")


class ToDoRead(ToDoBase):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ToDoListResponse(BaseModel):
    items: list[ToDoRead]


class MessageResponse(BaseModel):
    message: str
