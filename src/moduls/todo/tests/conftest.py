import asyncio
from datetime import datetime

import pytest
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from src.shared.base_repo import BaseRepository as ProjectBaseRepository
from src.shared.services.base_crud_service import BaseCRUDService  # noqa: E402

Base = declarative_base()


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    is_done = Column(Boolean, nullable=False, server_default=text("0"))
    is_deleted = Column(Boolean, nullable=False, server_default=text("0"), index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


@pytest.fixture(scope="session")
def event_loop():
    """
    Separate event loop for test session (important for Windows).
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture()
async def session(engine):
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as s:
        yield s


class ToDoRepository(ProjectBaseRepository[ToDo]):  # type: ignore[type-arg]
    def __init__(self, session: AsyncSession):
        super().__init__(session, ToDo)


class ToDoService(BaseCRUDService[ToDoRepository]):  # type: ignore[type-arg]
    pass


@pytest.fixture()
def repo(session) -> ToDoRepository:
    return ToDoRepository(session)


@pytest.fixture()
def service(repo) -> ToDoService:
    return ToDoService(repo)


@pytest.fixture()
def ToDoRepositoryClass():
    return ToDoRepository


@pytest.fixture()
def ToDoServiceClass():
    return ToDoService
