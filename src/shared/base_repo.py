from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic asynchronous repository providing basic CRUD operations.

    This class abstracts direct database interactions and can be inherited by
    domain-specific repositories (e.g., `ToDoRepository`). It uses SQLAlchemy's
    asynchronous session and supports Pydantic models as input for creation
    and update operations.

    Attributes:
        session (AsyncSession): Active SQLAlchemy asynchronous session.
        model (type[ModelType]): SQLAlchemy model class associated with this repository.
    """

    def __init__(self, session: AsyncSession, model: type[ModelType]):
        """
        Initialize a new repository instance.

        Args:
            session (AsyncSession): SQLAlchemy async session for DB operations.
            model (type[ModelType]): ORM model class this repository operates on.
        """
        self.session = session
        self.model = model

    async def create(self, data: BaseModel | dict) -> ModelType | None:
        """
        Create a new database record.

        Accepts a Pydantic model or dictionary, adds the corresponding ORM
        object to the database, commits the transaction, and refreshes it.

        Args:
            data (BaseModel | dict): The data to insert into the database.

        Returns:
            ModelType | None: The newly created ORM object or None if creation fails.
        """

        if isinstance(data, BaseModel):
            data = data.model_dump()
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def add_all(self, objects: list[Any]):
        """
        Add multiple ORM objects to the current session.

        The objects are added to the session but not committed automatically.

        Args:
            objects (list[Any]): List of ORM objects to add.
        """
        self.session.add_all(objects)

    async def get(self, obj_id: int, user_id: int | None = None) -> ModelType | None:
        """
        Retrieve a single record by ID, optionally filtered by user ID.

        Args:
            obj_id (int): The primary key of the record.
            user_id (int | None): Optional user ID for ownership validation.

        Returns:
            ModelType | None: The ORM object if found, otherwise None.
        """

        stmt = select(self.model).where(self.model.id == obj_id)

        if hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted.is_(False))

        if user_id is not None and hasattr(self.model, "user_id"):
            stmt = stmt.where(self.model.user_id == user_id)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self, user_id: int | None = None) -> list[ModelType]:
        """
        Retrieve all records, optionally filtered by user ID.

        Args:
            user_id (int | None): Optional user ID for filtering owned records.

        Returns:
            list[ModelType]: List of ORM objects.
        """

        stmt = select(self.model)
        if hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted.is_(False))
        if user_id is not None and hasattr(self.model, "user_id"):
            stmt = stmt.where(self.model.user_id == user_id)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, obj_id: int, data: dict, user_id: int) -> ModelType | None:
        """
        Update an existing record by ID.

        Retrieves the object, applies changes from a dictionary or Pydantic model,
        commits, and refreshes the object.

        Args:
            obj_id (int): The primary key of the record to update.
            data (dict | BaseModel): The data used to update the record.
            user_id (int): Optional user ID for ownership validation.

        Returns:
            ModelType | None: The updated ORM object, or None if not found.
        """
        obj = await self.get(obj_id)
        if not obj:
            return None
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int, user_id: int) -> bool:
        """
        Delete a record by ID.

        Args:
            obj_id (int): The primary key of the record to delete.
            user_id (int): Optional user ID for ownership validation.

        Returns:
            bool: True if the record was deleted, False if not found.
        """
        obj = await self.get(obj_id, user_id)
        if not obj:
            return False

        # Если есть поле is_deleted — делаем мягкое удаление
        if hasattr(obj, "is_deleted"):
            obj.is_deleted = True
            await self.session.commit()
            return True

        # Иначе физическое удаление
        await self.session.delete(obj)
        await self.session.commit()
        return True
