import pytest

from src.shared.services.base_get_service import base_get_service

pytestmark = pytest.mark.asyncio


async def test_base_get_service_returns_service_instance(
    session,
    ToDoServiceClass,
    ToDoRepositoryClass,
):
    get_todo_service = base_get_service(ToDoServiceClass, ToDoRepositoryClass)

    service_instance = await get_todo_service(session)  # type: ignore[arg-type]

    assert isinstance(service_instance, ToDoServiceClass)

    created = await service_instance.create({"title": "from-factory"}, user_id=123)
    assert created.user_id == 123
