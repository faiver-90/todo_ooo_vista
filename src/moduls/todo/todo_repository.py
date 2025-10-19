from src.shared.base_repo import BaseRepository
from src.shared.db.models.todo_model import ToDo


class ToDoRepository(BaseRepository[ToDo]):
    def __init__(self, db_session):
        super().__init__(db_session, ToDo)
