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


@todo_router_v1.post("", response_model=ToDoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_in: ToDoCreate,
    service: ToDoService = Depends(get_todo_service),
) -> ToDoRead:
    todo = await service.repo.create(todo_in)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create todo",
        )
    return todo


@todo_router_v1.get("", response_model=ToDoListResponse)
async def list_todos(
    service: ToDoService = Depends(get_todo_service),
) -> ToDoListResponse:
    todos = await service.list()
    return ToDoListResponse(items=todos)


@todo_router_v1.get("/{todo_id}", response_model=ToDoRead)
async def get_todo(
    todo_id: int,
    service: ToDoService = Depends(get_todo_service),
) -> ToDoRead:
    todo = await service.get(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found"
        )
    return todo


@todo_router_v1.patch("/{todo_id}", response_model=ToDoRead)
async def update_todo(
    todo_id: int,
    todo_in: ToDoUpdate,
    service: ToDoService = Depends(get_todo_service),
) -> ToDoRead:
    todo = await service.update(todo_id, todo_in)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found"
        )
    return todo


@todo_router_v1.post("/{todo_id}/complete", response_model=ToDoRead)
async def mark_todo_completed(
    todo_id: int,
    service: ToDoService = Depends(get_todo_service),
) -> ToDoRead:
    todo = await service.update(todo_id, {"is_completed": True})
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found"
        )
    return todo


@todo_router_v1.delete("/{todo_id}", response_model=MessageResponse)
async def delete_todo(
    todo_id: int,
    service: ToDoService = Depends(get_todo_service),
) -> MessageResponse:
    deleted = await service.delete(todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found"
        )
    return MessageResponse(message="ToDo deleted")
