# src/shared/db/session.py
from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import contextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

from src.shared.db.engine import get_async_engine, get_sync_engine

# ленивые фабрики sessionmaker — создаются при первом вызове
AsyncSessionLocal = async_sessionmaker(
    bind=get_async_engine(),
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Depends-провайдер асинхронной сессии.
    """
    async with AsyncSessionLocal() as session:
        yield session


@contextmanager
def get_sync_session() -> Session:
    """
    Синхронная сессия для скриптов/миграций.
    """
    SessionLocal = sessionmaker(bind=get_sync_engine())
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
