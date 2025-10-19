from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.moduls.todo.api.v1.services.todo_service import ToDoService
from src.shared.configs.get_settings import get_settings
from src.shared.db.session import get_async_session


async def get_todo_service(
    db: AsyncSession = Depends(get_async_session),
) -> ToDoService:
    return ToDoService(
        settings=get_settings(),
    )
