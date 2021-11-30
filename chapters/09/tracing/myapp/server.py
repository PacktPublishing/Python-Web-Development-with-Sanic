from sanic import Request, Sanic, json
from myapp.common.log import setup_logging, app_logger


def create_app():
    app = Sanic(__name__)
    setup_logging(app)

    @app.route("")
    async def dummy(request: Request):
        app_logger.debug("This is a DEBUG message")
        app_logger.info("This is a INFO message")
        app_logger.warning("This is a WARNING message")
        app_logger.error("This is a ERROR message")
        app_logger.critical("This is a CRITICAL message")
        return json(
            {
                "requests_count": request.protocol.state["requests_count"],
                "request_id": str(request.id),
                "conn_id": id(request.conn_info),
                "email": request.headers.get("x-goog-authenticated-user-email"),
            }
        )

    from myapp.middleware import request_context  # noqa

    return app
