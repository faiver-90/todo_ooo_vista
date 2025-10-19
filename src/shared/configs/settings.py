from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Единая типизированная конфигурация приложения.
    Значения берутся из .env, при отсутствии — используются дефолты ниже.
    """

    postgres_user: str = Field("pgres", alias="POSTGRES_USER")
    postgres_password: str = Field("pgres", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field("pgres", alias="POSTGRES_DB")
    postgres_host: str = Field("db", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    database_url: str | None = Field(None, alias="DATABASE_URL")
    sync_database_url: str | None = Field(None, alias="SYNC_DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings: Settings = Settings()  # type: ignore[call-arg]
