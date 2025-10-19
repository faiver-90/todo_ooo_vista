from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from src.shared.configs.get_settings import get_settings

settings = get_settings()

async_engine_options: dict[str, object] = {
    "echo": settings.debug_db,
    "future": True,
    "pool_pre_ping": True,
}

if settings.use_pgbouncer:
    async_engine_options.update({"poolclass": NullPool})
else:
    async_engine_options.update(
        {
            "pool_size": 20,
            "max_overflow": 10,
            "pool_timeout": 30,
            "pool_recycle": 1800,
        }
    )

async_engine = create_async_engine(  # type: ignore[arg-type]
    settings.database_url,
    **async_engine_options,
)

sync_engine_options: dict[str, object] = {
    "echo": settings.debug_db,
}

if settings.use_pgbouncer:
    sync_engine_options.update({"poolclass": NullPool, "pool_pre_ping": True})

sync_engine = create_engine(  # type: ignore[arg-type]
    settings.sync_database_url,
    **sync_engine_options,
)
