from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from src.shared.configs.get_settings import get_settings


def _resolve_urls() -> tuple[str, str]:
    """
    Возвращает (ASYNC_URL, SYNC_URL) с приоритетом:
    1) Тесты: TESTING=1 -> DATABASE_URL / SYNC_DATABASE_URL или sqlite по умолчанию
    2) ENV: DATABASE_URL / SYNC_DATABASE_URL
    3) settings: settings.database_url / settings.sync_database_url
    """
    settings = get_settings()
    testing = os.getenv("TESTING") == "1"

    if testing:
        async_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
        sync_url = os.getenv("SYNC_DATABASE_URL", "sqlite:///:memory:")
        return async_url, sync_url

    async_url = os.getenv("DATABASE_URL", str(settings.database_url))
    sync_url = os.getenv("SYNC_DATABASE_URL", str(settings.sync_database_url))
    return async_url, sync_url


def _async_engine_options() -> dict[str, Any]:
    settings = get_settings()
    opts: dict[str, Any] = {
        "echo": settings.debug_db,
        "future": True,
        "pool_pre_ping": True,
    }

    async_url, _ = _resolve_urls()

    # Если PgBouncer – без собственного пула
    if settings.use_pgbouncer:
        opts["poolclass"] = NullPool
    else:
        # Для SQLite пулы не нужны/вредны
        if not async_url.startswith("sqlite+aiosqlite"):
            opts.update(
                {
                    "pool_size": 20,
                    "max_overflow": 10,
                    "pool_timeout": 30,
                    "pool_recycle": 1800,
                }
            )
    return opts


def _sync_engine_options() -> dict[str, Any]:
    settings = get_settings()
    opts: dict[str, Any] = {"echo": settings.debug_db}
    if settings.use_pgbouncer:
        opts.update({"poolclass": NullPool, "pool_pre_ping": True})
    return opts


@lru_cache(maxsize=1)
def get_async_engine() -> AsyncEngine:
    async_url, _ = _resolve_urls()
    return create_async_engine(async_url, **_async_engine_options())


@lru_cache(maxsize=1)
def get_sync_engine() -> Engine:
    _, sync_url = _resolve_urls()
    return create_engine(sync_url, **_sync_engine_options())
