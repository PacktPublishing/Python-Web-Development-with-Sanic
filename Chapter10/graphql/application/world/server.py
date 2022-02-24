from sanic import Sanic

from world.common.log import setup_logging


def create_app() -> Sanic:
    app = Sanic("GraphQLApp")
    setup_logging(app)

    from world.blueprints.view import bp  # noqa
    from world.middleware import request_context  # noqa
    from world.worker import postgres  # noqa

    app.blueprint(bp)

    return app
