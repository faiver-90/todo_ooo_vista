from functools import lru_cache

from src.shared.configs.settings import Settings


@lru_cache
def get_settings() -> Settings:
    """
    Cached dependency that provides application settings.

    Uses LRU cache to ensure the Settings object is created only once
    and reused throughout the application lifecycle.

    Returns:
        Settings: The cached instance of application configuration.
    """
    return Settings()  # type: ignore
