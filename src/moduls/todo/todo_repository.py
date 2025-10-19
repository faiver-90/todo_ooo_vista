from src.shared.base_repo import BaseRepository
from src.shared.db.models.todo_model import ToDo


class ToDoRepository(BaseRepository[ToDo]):
    """
    Repository class for managing database operations related to ToDo entities.

    Provides an abstraction layer between the database and the service layer,
    built on top of the generic BaseRepository.

    This class is responsible for CRUD operations specific to the `ToDo` model
    and can be extended with custom queries or domain-specific logic.

    Inherits:
        BaseRepository[ToDo]: Generic base repository that provides standard
        create, read, update, and delete functionality.

    Args:
        db_session (AsyncSession): The SQLAlchemy asynchronous session used for
        executing database operations.
    """

    def __init__(self, db_session):
        super().__init__(db_session, ToDo)
