from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Declarative base class for all SQLAlchemy ORM models.

    All database models in the project should inherit from this class.
    It defines the shared metadata and provides a consistent ORM foundation.
    """

    pass
