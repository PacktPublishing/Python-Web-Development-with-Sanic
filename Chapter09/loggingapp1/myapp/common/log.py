import logging
import sys

from sanic import Sanic
from sanic.log import error_logger, logger

app_logger = logging.getLogger("myapplogger")


DEFAULT_LOGGING_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s"
)
DEFAULT_LOGGING_DATEFORMAT = "%Y-%m-%d %H:%M:%S %z"


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[34m",
        "WARNING": "\033[01;33m",
        "ERROR": "\033[01;31m",
        "CRITICAL": "\033[02;47m\033[01;31m",
    }

    def format(self, record) -> str:
        prefix = self.COLORS.get(record.levelname)
        message = super().format(record)

        if prefix:
            message = f"{prefix}{message}\033[0m"

        return message


def setup_logging(app: Sanic):
    environment = app.config.get("ENVIRONMENT", "local")
    logging_level = app.config.get(
        "LOGGING_LEVEL",
        logging.DEBUG if environment == "local" else logging.INFO,
    )
    fmt = app.config.get("LOGGING_FORMAT", DEFAULT_LOGGING_FORMAT)
    datefmt = app.config.get("LOGGING_DATEFORMAT", DEFAULT_LOGGING_DATEFORMAT)
    formatter = _get_formatter(environment == "local", fmt, datefmt)

    # Setup application logger
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    app_logger.addHandler(handler)
    app_logger.setLevel(logging_level)

    # Output logs to file in production
    if app.config.get("ENVIRONMENT", "local") == "production":
        file_handler = logging.FileHandler("output.log")
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)

    # Apply the same logging handlers to Sanic's logging instances
    logger.handlers = app_logger.handlers
    error_logger.handlers = app_logger.handlers


def _get_formatter(is_local, fmt, datefmt):
    formatter_type = logging.Formatter
    if is_local and sys.stdout.isatty():
        formatter_type = ColorFormatter

    return formatter_type(
        fmt=fmt,
        datefmt=datefmt,
    )
