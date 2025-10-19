from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# def _build_psycopg_url(
#     user: str,
#     password: str,
#     host: str = "localhost",
#     port: int = 5432,
#     db: str = "pgres",
# ) -> str:
#     """Собирает psycopg DSN, если DATABASE_URL не задан явно."""
#     return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"


# def _build_psycopg2_url(
#     user: str,
#     password: str,
#     host: str = "localhost",
#     port: int = 5432,
#     db: str = "pgres",
# ) -> str:
#     """Собирает sync DSN, если SYNC_DATABASE_URL не задан явно."""
#     return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


class Settings(BaseSettings):
    """
    Единая типизированная конфигурация приложения.
    Значения берутся из .env, при отсутствии — используются дефолты ниже.
    """

    debug_db: bool = Field(False, alias="DEBUG_DB")

    # === Databases (части + готовые DSN) ===
    postgres_user: str = Field("pgres", alias="POSTGRES_USER")
    postgres_password: str = Field("pgres", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field("pgres", alias="POSTGRES_DB")
    postgres_host: str = Field("db", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    # Если явно заданы — используем их; иначе соберём из частей выше
    database_url: str | None = Field(None, alias="DATABASE_URL")
    sync_database_url: str | None = Field(None, alias="SYNC_DATABASE_URL")

    # === Redis ===
    redis_password: str | None = Field(None, alias="REDIS_PASSWORD")
    default_redis_url: str = Field(
        "redis://localhost:6379/0", alias="DEFAULT_REDIS_URL"
    )
    redis_url_env: str = Field("redis://localhost:6379/0", alias="REDIS_URL_ENV")
    celery_broker_url: str = Field(
        "redis://localhost:6379/0", alias="CELERY_BROKER_URL"
    )
    celery_result_backend: str = Field(
        "redis://localhost:6379/1", alias="CELERY_RESULT_BACKEND"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # @model_validator(mode="after")
    # def _fill_derived_values(self) -> Settings:
    #     if not self.database_url:
    #         self.database_url = _build_psycopg_url(
    #             self.postgres_user,
    #             self.postgres_password,
    #             self.postgres_host,
    #             self.postgres_port,
    #             self.postgres_db,
    #         )
    #     if not self.sync_database_url:
    #         self.sync_database_url = _build_psycopg2_url(
    #             self.postgres_user,
    #             self.postgres_password,
    #             self.postgres_host,
    #             self.postgres_port,
    #             self.postgres_db,
    #         )
    #     return self


settings: Settings = Settings()  # type: ignore[call-arg]
