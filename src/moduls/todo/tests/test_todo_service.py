import pytest
from sqlalchemy import select

pytestmark = pytest.mark.asyncio


async def test_create_injects_user_id_when_missing(service, repo, session):
    created = await service.create({"title": "A"}, user_id=10)

    assert created.id is not None
    assert created.user_id == 10
    assert created.title == "A"
    assert created.is_deleted is False

    rows = (await session.execute(select(type(created)))).scalars().all()
    assert len(rows) == 1


async def test_create_preserves_user_id_if_provided(service, session):
    created = await service.create({"title": "B", "user_id": 77}, user_id=10)
    assert created.user_id == 77
    row = (
        await session.execute(
            select(type(created)).where(created.id == type(created).id)
        )
    ).scalar_one()
    assert row.user_id == 77


async def test_list_excludes_soft_deleted_and_filters_by_user(service, repo, session):
    a = await service.create({"title": "task-a"}, user_id=1)
    b = await service.create({"title": "task-b"}, user_id=1)
    c = await service.create({"title": "task-c"}, user_id=2)

    ok = await service.delete(b.id, user_id=1)
    assert ok is True

    items_user1 = await service.list(user_id=1)

    ids_user1 = {x.id for x in items_user1}
    assert a.id in ids_user1
    assert b.id not in ids_user1
    assert c.id not in ids_user1

    items_all = await service.list()
    ids_all = {x.id for x in items_all}
    assert b.id not in ids_all


async def test_update_changes_fields(service):
    r = await service.create({"title": "Old"}, user_id=1)
    updated = await service.update(r.id, {"title": "New"}, user_id=1)
    assert updated is not None
    assert updated.title == "New"


async def test_delete_marks_is_deleted_true(service, repo, session):
    r = await service.create({"title": "TBD"}, user_id=1)

    ok = await service.delete(r.id, user_id=1)
    assert ok is True

    model = type(r)
    row = (await session.execute(select(model).where(model.id == r.id))).scalar_one()
    assert row.is_deleted is True

    items = await service.list()
    ids = {x.id for x in items}
    assert r.id not in ids
