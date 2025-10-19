from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Strongly typed global application configuration.

    Reads environment variables from the `.env` file or system environment.
    Provides connection details for PostgreSQL and other core settings.

    Attributes:
        postgres_user (str): PostgreSQL username.
        postgres_password (str): PostgreSQL password.
        postgres_db (str): PostgreSQL database name.
        postgres_host (str): Host address for the PostgreSQL server.
        postgres_port (int): Port number for PostgreSQL (default: 5432).
        database_url (str | None): Full async database URL (if defined).
        sync_database_url (str | None): Full sync database URL (if defined).
        debug_db (bool): Enable SQLAlchemy engine echo for debugging.
        use_pgbouncer (bool): Flag to switch SQLAlchemy engines into NullPool mode when using PgBouncer.

    Config:
        env_file (str): Path to the `.env` file.
        env_file_encoding (str): Encoding of the environment file.
        case_sensitive (bool): Whether environment variable names are case-sensitive.
        extra (str): Behavior for unknown fields (ignored).
    """

    postgres_user: str = Field("pgres", alias="POSTGRES_USER")
    postgres_password: str = Field("pgres", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field("pgres", alias="POSTGRES_DB")
    postgres_host: str = Field("db", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    database_url: str | None = Field(None, alias="DATABASE_URL")
    sync_database_url: str | None = Field(None, alias="SYNC_DATABASE_URL")
    debug_db: bool = Field(False, alias="DEBUG_DB")
    use_pgbouncer: bool = Field(False, alias="USE_PGBOUNCER")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings: Settings = Settings()  # type: ignore[call-arg]
