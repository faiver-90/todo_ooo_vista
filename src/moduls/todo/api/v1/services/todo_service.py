from src.moduls.todo.todo_repository import ToDoRepository
from src.shared.services.base_crud_service import BaseCRUDService


class ToDoService(BaseCRUDService[ToDoRepository]):
    """
    Service layer for handling business logic related to ToDo entities.

    Extends the generic BaseCRUDService with a concrete ToDoRepository implementation.
    Acts as an intermediary between the API layer (routers) and the data access layer (repository),
    allowing for additional business rules, validations, or transformations to be added later.

    Inherits:
        BaseCRUDService[ToDoRepository]: Provides generic CRUD operations for ToDo objects.
    """

    pass
