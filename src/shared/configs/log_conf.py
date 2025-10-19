from logging.config import dictConfig
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logger() -> None:
    """
    Configure application-wide logging using the built-in logging system.

    Sets up rotating file handlers for application and error logs, defines
    human-readable and JSON formatters, and assigns handlers to custom loggers.

    Log files:
        - app.log: General application logs (INFO level and above)
        - errors.log: Error logs (ERROR level and above)

    The log configuration includes:
        - Two formatters (plain text and JSON)
        - RotatingFileHandler for each log type
        - Logger definitions: 'app_log' and 'errors_log'
    """
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "[{asctime}] {levelname}: {name}: {message}",
                    "style": "{",
                },
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                },
            },
            "handlers": {
                "app": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "app.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "INFO",
                },
                "errors": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(LOG_DIR / "errors.log"),
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "ERROR",
                },
            },
            "loggers": {
                "app_log": {"handlers": ["app"], "level": "DEBUG", "propagate": False},
                "errors_log": {
                    "handlers": ["errors"],
                    "level": "DEBUG",
                    "propagate": False,
                },
            },
        }
    )
