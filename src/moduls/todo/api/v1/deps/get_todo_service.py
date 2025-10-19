from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.moduls.todo.api.v1.services.todo_service import ToDoService
from src.shared.configs.get_settings import get_settings
from src.shared.db.session import get_async_session


async def get_todo_service(
    db: AsyncSession = Depends(get_async_session),
) -> ToDoService:
    """
    Dependency provider that returns a ToDoService instance.

    Initializes and provides a new instance of the ToDoService
    with the current application settings and an active database session.

    Args:
        db (AsyncSession): SQLAlchemy asynchronous session, injected by FastAPI's dependency system.

    Returns:
        ToDoService: The service object responsible for ToDo business logic and database operations.
    """
    return ToDoService(
        settings=get_settings(),
    )
