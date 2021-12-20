import logging

from sanic import Sanic
from sanic.log import error_logger, logger

app_logger = logging.getLogger("myapplogger")


DEFAULT_LOGGING_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s"
)


def setup_logging(app: Sanic):
    formatter = logging.Formatter(
        fmt=app.config.get("LOGGING_FORMAT", DEFAULT_LOGGING_FORMAT),
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )

    # Setup application logger
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    app_logger.addHandler(handler)

    # Output logs to file in production
    if app.config.get("ENVIRONMENT", "local") == "production":
        file_handler = logging.FileHandler("output.log")
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)

    # Apply the same logging handlers to Sanic's logging instances
    logger.handlers = app_logger.handlers
    error_logger.handlers = app_logger.handlers
