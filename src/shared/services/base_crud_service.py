from typing import Generic, TypeVar

RepoType = TypeVar("RepoType")


class BaseCRUDService(Generic[RepoType]):
    """
    Generic service layer providing high-level CRUD operations.

    This class serves as an abstraction over repository-level operations,
    adding lightweight business logic such as automatic user assignment
    and centralized method access for API handlers.

    It is meant to be inherited by domain-specific services (e.g., `ToDoService`).

    Attributes:
        repo (RepoType): The repository instance handling database operations.
    """

    def __init__(self, repo: RepoType):
        """
        Initialize a CRUD service with the given repository.

        Args:
            repo (RepoType): Repository instance responsible for database interactions.
        """
        self.repo = repo

    async def create(self, data, user_id=None):
        """
        Create a new record.

        Automatically injects the `user_id` into the data payload if missing,
        then delegates the creation to the repository.

        Args:
            data (dict): Data for creating the record.
            user_id (int | None): Optional user ID associated with the record.

        Returns:
            Any: The created record returned by the repository.
        """
        if not data.get("user_id") or data["user_id"] == 0:
            data["user_id"] = user_id
        return await self.repo.create(data)

    async def get(self, obj_id: int, user_id=None):
        """
        Retrieve a single record by ID.

        Delegates the operation to the underlying repository.

        Args:
            obj_id (int): The primary key of the record.
            user_id (int | None): Optional user ID for ownership validation.

        Returns:
            Any: The retrieved record or None if not found.
        """
        return await self.repo.get(obj_id, user_id)

    async def list(self, user_id: int | None = None):
        """
        Retrieve a list of records.

        Delegates the operation to the repository, optionally filtering by user.

        Args:
            user_id (int | None): Optional user ID for filtering.

        Returns:
            list[Any]: A list of retrieved records.
        """
        return await self.repo.list(user_id)

    async def update(self, obj_id: int, data: dict, user_id: int | None = None):
        """
        Update an existing record.

        Delegates the update operation to the repository.

        Args:
            obj_id (int): The primary key of the record to update.
            data (dict): The data used to update the record.
            user_id (int | None): Optional user ID for ownership validation.

        Returns:
            Any | None: The updated record, or None if not found.
        """
        return await self.repo.update(obj_id, data, user_id)

    async def delete(self, obj_id: int, user_id: int | None = None):
        """
        Delete a record by ID.

        Delegates the deletion operation to the repository.

        Args:
            obj_id (int): The primary key of the record to delete.
            user_id (int | None): Optional user ID for ownership validation.

        Returns:
            bool: True if deletion succeeded, False otherwise.
        """
        return await self.repo.delete(obj_id, user_id)
