from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from src.moduls.todo.api.v1.todo_router import todo_router_v1
from src.shared.configs.log_conf import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    yield


def get_app() -> FastAPI:
    app_init = FastAPI(version="1.0.0", docs_url="/swagger", lifespan=lifespan)

    from sqlalchemy import text
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.shared.db.session import get_async_session

    @app_init.get(
        "/health_check",
        summary="Проверка работоспособности приложения и базы данных",
        description="Возвращает статус работы сервера и подключения к базе данных.",
        tags=["Service"],
    )
    async def health_check(
        session: AsyncSession = Depends(get_async_session),
    ) -> dict[str, str]:
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
