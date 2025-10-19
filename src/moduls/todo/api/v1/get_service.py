from src.moduls.todo.api.v1.services.todo_service import ToDoService
from src.moduls.todo.todo_repository import ToDoRepository
from src.shared.services.base_get_service import base_get_service

get_todo_service = base_get_service(ToDoService, ToDoRepository)
