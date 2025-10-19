from collections.abc import AsyncGenerator
from contextlib import contextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from src.shared.db.engine import async_engine, sync_engine

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an asynchronous SQLAlchemy session.

    Yields a single instance of AsyncSession, ensuring proper
    connection management within FastAPI routes and services.

    Yields:
        AsyncGenerator[AsyncSession, None]: Active asynchronous database session.
    """
    async with AsyncSessionLocal() as session:
        yield session


@contextmanager
def get_sync_session():
    """
    Context manager for creating and closing a synchronous SQLAlchemy session.

    Intended for use in scripts, migrations, or background tasks that
    require blocking (non-async) database access.

    Yields:
        Session: Active synchronous SQLAlchemy session.
    """
    SessionLocal = sessionmaker(bind=sync_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
