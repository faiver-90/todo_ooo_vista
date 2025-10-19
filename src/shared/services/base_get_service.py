from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.db.session import get_async_session


def base_get_service(service_class, repo_class, *extra_args):
    """
    Factory function that generates a FastAPI dependency for creating service instances.

    This utility dynamically constructs a dependency function that:
      1. Injects a database session using FastAPI's dependency system.
      2. Initializes the specified repository with that session.
      3. Instantiates the given service class, passing the repository (and any extra arguments).

    Commonly used to reduce repetitive dependency wiring for services and repositories.

    Example:
        ```python
        get_todo_service = base_get_service(ToDoService, ToDoRepository)


        @router.get("/todos")
        async def list_todos(service: ToDoService = Depends(get_todo_service)):
            return await service.list()
        ```

    Args:
        service_class: The service class to instantiate (e.g., `ToDoService`).
        repo_class: The repository class to instantiate (e.g., `ToDoRepository`).
        *extra_args: Optional additional arguments to pass to the service constructor.

    Returns:
        Callable: A dependency function that FastAPI can use to inject a service instance.
    """

    async def _get(session: AsyncSession = Depends(get_async_session)):
        repo = repo_class(session)
        return service_class(repo, *extra_args)

    return _get
