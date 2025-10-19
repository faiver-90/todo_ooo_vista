# ToDo OOO Vista

Сервис для управления ежедневными задачами: создавайте, просматривайте, обновляйте и удаляйте заметки, отмечайте их выполненными. Реализован на FastAPI и асинхронном SQLAlchemy с PostgreSQL.

## Возможности
- Создание, чтение, обновление и удаление задач
- Просмотр списка задач с отображением статуса выполнения
- Отдельный эндпоинт для отметки задачи завершённой
- Отслеживание времени создания и изменений

## Технологии
- FastAPI
- SQLAlchemy (async)
- PostgreSQL (psycopg)
- Poetry (управление зависимостями)

## Требования
- Python 3.14
- PostgreSQL 14+

## Переменные окружения
Создайте .env:
`
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=pgres
POSTGRES_PASSWORD=pgres
POSTGRES_DB=pgres
DATABASE_URL=postgresql+psycopg://pgres:pgres@localhost:5432/pgres
`

## Локальный запуск
1. Установите Poetry (если ещё не установлен): pip install poetry
2. Установите зависимости: poetry install
3. Примените миграции: poetry run alembic upgrade head
4. Запустите приложение: poetry run uvicorn src.main_app.init_app:app --reload
5. Документация будет доступна по адресу: http://localhost:8001/swagger

## Эндпоинты API
- POST /todos — создать новую задачу
- GET /todos — получить список задач
- GET /todos/{todo_id} — получить задачу по идентификатору
- PATCH /todos/{todo_id} — обновить название, описание или статус задачи
- POST /todos/{todo_id}/complete — отметить задачу выполненной
- DELETE /todos/{todo_id} — удалить задачу

Успешные ответы (200) соответствуют схемам из src/moduls/todo/api/v1/schemas.py. Ошибки возвращаются в стандартном формате FastAPI.

## Разработка
- Тесты: poetry run pytest
- Линтеры: poetry run ruff check .


