import logging
import sys
from functools import partial
from typing import Any, cast

from sanic import Sanic

app_logger = logging.getLogger("myapplogger")


class CustomFormatter(logging.Formatter):
    _fmt = (
        "[%(asctime)s] [%(name)s:%(levelname)s] [%(filename)s:%(lineno)s] %(message)s"
    )


DEFAULT_LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s] %(request_info)s%(message)s"
DEFAULT_LOGGING_DATEFORMAT = "%Y-%m-%d %H:%M:%S %z"
old_factory = logging.getLogRecordFactory()


class RequestInfoLogRecord(logging.LogRecord):
    request_info: str


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[34m",
        "WARNING": "\033[01;33m",
        "ERROR": "\033[01;31m",
        "CRITICAL": "\033[02;47m\033[01;31m",
    }

    def format(self, record: logging.LogRecord) -> str:
        prefix = self.COLORS.get(record.levelname)
        message = super().format(record)

        if prefix:
            message = f"{prefix}{message}\033[0m"

        return message


def _get_formatter(is_local: bool, fmt: str, datefmt: str) -> logging.Formatter:
    formatter_type = logging.Formatter
    if is_local and sys.stdout.isatty():
        formatter_type = ColorFormatter

    return formatter_type(
        fmt=fmt,
        datefmt=datefmt,
    )


def _record_factory(*args: Any, app: Sanic, **kwargs: Any) -> RequestInfoLogRecord:
    record = cast(RequestInfoLogRecord, old_factory(*args, **kwargs))
    record.request_info = ""

    if hasattr(app.ctx, "request"):
        request = app.ctx.request.get(None)
        if request:
            display = " ".join([str(request.id), request.method, request.path])
            record.request_info = f"[{display}] "

    return record


def setup_logging(app: Sanic) -> None:
    environment = app.config.get("ENVIRONMENT", "local")
    logging_level = app.config.get(
        "LOGGING_LEVEL", logging.DEBUG if environment == "local" else logging.INFO
    )
    fmt = app.config.get("LOGGING_FORMAT", DEFAULT_LOGGING_FORMAT)
    datefmt = app.config.get("LOGGING_DATEFORMAT", DEFAULT_LOGGING_DATEFORMAT)
    formatter = _get_formatter(environment == "local", fmt, datefmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    app_logger.addHandler(handler)
    app_logger.setLevel(logging_level)

    if environment == "production":
        file_handler = logging.FileHandler("output.log")
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)

    logging.setLogRecordFactory(partial(_record_factory, app=app))

    logger_tortoise = logging.getLogger("tortoise")
    logger_tortoise.setLevel(logging.DEBUG)
    logger_tortoise.addHandler(handler)
