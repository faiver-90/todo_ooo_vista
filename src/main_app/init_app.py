from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from src.moduls.todo.api.v1.todo_router import todo_router_v1
from src.shared.configs.log_conf import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager executed during the startup and shutdown phases of the FastAPI application.

    Initializes application-wide logging before the server starts
    and performs cleanup when the application stops.

    Args:
        app (FastAPI): The current FastAPI application instance.

    Yields:
        None: Control is passed to the application runtime.
    """
    setup_logger()
    yield


def get_app() -> FastAPI:
    """
    Initialize and return the FastAPI application instance.

    Creates and configures the FastAPI app, registers routers,
    sets up logging, and adds a health check endpoint.
    The Swagger documentation is available at `/swagger`.

    Returns:
        FastAPI: The fully configured FastAPI application instance.
    """
    app_init = FastAPI(version="1.0.0", docs_url="/swagger", lifespan=lifespan)

    from sqlalchemy import text
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.shared.db.session import get_async_session

    @app_init.get(
        "/health_check",
        summary="Checking the functionality of the application and database",
        description="Returns the status of the server and database connection..",
        tags=["Service"],
    )
    async def health_check(
        session: AsyncSession = Depends(get_async_session),
    ) -> dict[str, str]:
        """
        Check the health of the application and database connection.

        Executes a simple SQL query (`SELECT 1`) using the provided async
        SQLAlchemy session.
        Returns `"ok"` if the database is reachable, otherwise `"error"` with
        the corresponding exception message.

        Args:
            session (AsyncSession): The async SQLAlchemy session dependency.

        Returns:
            dict[str, str]: A dictionary containing the application
            and database status.
        """
        try:
            await session.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}
        except SQLAlchemyError as e:
            return {"status": "error", "database": f"unavailable: {str(e)}"}
        except Exception as e:
            return {"status": "error", "database": f"unavailable: {str(e)}"}

    app_init.include_router(todo_router_v1)
    return app_init


app = get_app()
