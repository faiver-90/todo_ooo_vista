from fastapi import APIRouter, Depends, HTTPException, status

from src.moduls.todo.api.v1.get_service import get_todo_service
from src.moduls.todo.api.v1.schemas import (
    MessageResponse,
    ToDoCreate,
    ToDoListResponse,
    ToDoRead,
    ToDoUpdate,
)
from src.moduls.todo.api.v1.services.todo_service import ToDoService

todo_router_v1 = APIRouter(prefix="/todos", tags=["ToDo"])


@todo_router_v1.post(
    "",
    response_model=ToDoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a todo",
    description="Create a new todo item and return the persisted entity.",
)
async def create_todo(
    todo_in: ToDoCreate,
    service: ToDoService = Depends(get_todo_service),
) -> ToDoRead:
    """Persist a new todo item and return the created instance."""
    todo = await service.repo.create(todo_in)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create todo",
        )
    return todo


@todo_router_v1.get(
    "",
    response_model=ToDoListResponse,
    summary="List todos",
    description="Retrieve the collection of todo items with minimal metadata.",
)
async def list_todos(
    service: ToDoService = Depends(get_todo_service),
) -> ToDoListResponse:
    """Return the list of todos available to the current context."""
    todos = await service.list()
    return ToDoListResponse(items=todos)


@todo_router_v1.get(
    "/{todo_id}",
    response_model=ToDoRead,
    summary="Get todo",
    description="Fetch a todo item by its identifier.",
)
async def get_todo(
    todo_id: int,
    service: ToDoService = Depends(get_todo_service),
) -> ToDoRead:
    """Return a single todo by identifier or raise a not found error."""
    todo = await service.get(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found"
        )
    return todo


@todo_router_v1.patch(
    "/{todo_id}",
    response_model=ToDoRead,
    summary="Update todo",
    description="Apply partial updates to a todo item.",
)
async def update_todo(
    todo_id: int,
    todo_in: ToDoUpdate,
    service: ToDoService = Depends(get_todo_service),
) -> ToDoRead:
    """Update selected fields of a todo and return the modified entity."""
    todo = await service.update(todo_id, todo_in)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found"
        )
    return todo


@todo_router_v1.post(
    "/{todo_id}/complete",
    response_model=ToDoRead,
    summary="Mark todo as complete",
    description="Set the completion flag for a todo item and return the updated entity.",
)
async def mark_todo_completed(
    todo_id: int,
    service: ToDoService = Depends(get_todo_service),
) -> ToDoRead:
    """Mark the todo as completed and return the updated instance."""
    todo = await service.update(todo_id, {"is_completed": True})
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found"
        )
    return todo


@todo_router_v1.delete(
    "/{todo_id}",
    response_model=MessageResponse,
    summary="Delete todo",
    description="Remove a todo item and confirm the deletion.",
)
async def delete_todo(
    todo_id: int,
    service: ToDoService = Depends(get_todo_service),
) -> MessageResponse:
    """Delete the todo and return a confirmation message."""
    deleted = await service.delete(todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found"
        )
    return MessageResponse(message="ToDo deleted")
