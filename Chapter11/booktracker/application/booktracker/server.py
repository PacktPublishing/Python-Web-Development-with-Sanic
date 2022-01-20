from pathlib import Path
from typing import Optional, Sequence, Tuple

from sanic import Sanic

# Modules imported here should NOT have a Sanic.get_app() call in the global
# scope. Doing so will cause a circular import. Therefore, we progromatically
# import those modules inside of the create_app() factory.
from booktracker.common.auth.startup import setup_auth
from booktracker.common.csrf import setup_csrf
from booktracker.common.log import setup_logging
from booktracker.common.pagination import setup_pagination
from booktracker.worker.module import setup_modules
from booktracker.worker.request import BooktrackerRequest

DEFAULT: Tuple[str, ...] = (
    "booktracker.blueprints.view",
    "booktracker.middleware.request_context",
    "booktracker.worker.postgres",
    "booktracker.worker.redis",
)


def create_app(module_names: Optional[Sequence[str]] = None) -> Sanic:
    """
    Application factory: responsible for gluing all of the pieces of the
    application together. In most use cases, running the application will be
    done will a None value for module_names. Therefore, we provide a default
    list. This provides flexibility when unit testing the application. The main
    purpose for this pattern is to avoide import issues. This should be the
    first thing that is called.
    """
    if module_names is None:
        module_names = DEFAULT

    app = Sanic("BooktrackerApp", request_class=BooktrackerRequest)
    app.config.UI_DIR = Path(__file__).parent.parent / "ui"
    app.config.CORS_ORIGINS = "http://localhost:7777"
    app.config.CSRF_REF_PADDING = 12
    app.config.CSRF_REF_LENGTH = 18

    setup_logging(app)
    setup_pagination(app)
    setup_auth(app)
    setup_modules(app, *module_names)
    setup_csrf(app)

    return app
