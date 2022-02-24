from typing import Optional, Sequence
from sanic import Sanic


from .autodiscovery import autodiscover

DEFAULT_BLUEPRINTS = [
    "src.blueprints.v1.book.view",
    "src.blueprints.v1.author.view",
    "src.blueprints.v2.group",
]


def create_app(
    init_blueprints: Optional[Sequence[str]] = None,
) -> Sanic:
    app = Sanic("BookTracker")

    if not init_blueprints:
        init_blueprints = DEFAULT_BLUEPRINTS

    autodiscover(app, *init_blueprints)

    return app
