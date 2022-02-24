from .utilities.app_factory import create_app
from sanic.log import logger

app = create_app()


@app.main_process_start
def display_routes(app, _):
    logger.info("Registered routes:")
    for route in app.router.routes:
        logger.info(f"> /{route.path}")
