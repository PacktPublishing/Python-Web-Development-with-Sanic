from sanic import Sanic, text

from myapp.common.log import app_logger, setup_logging


def create_app():
    app = Sanic(__name__)
    setup_logging(app)

    @app.route("")
    async def dummy(_):
        app_logger.debug("This is a DEBUG message")
        app_logger.info("This is a INFO message")
        app_logger.warning("This is a WARNING message")
        app_logger.error("This is a ERROR message")
        app_logger.critical("This is a CRITICAL message")
        return text("")

    return app
