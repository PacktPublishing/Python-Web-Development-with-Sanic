from sanic import Sanic
from feeder.common.log import setup_logging


def create_app():
    app = Sanic(__name__)
    setup_logging(app)

    from feeder.middleware import request_context  # noqa
    from feeder.blueprints.view import bp  # noqa
    from feeder.worker import redis  # noqa

    app.blueprint(bp)

    return app
