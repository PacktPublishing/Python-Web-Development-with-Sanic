from logging import getLogger
from pathlib import Path

from sanic import Blueprint, Request
from sanic.response import file

from .reload import setup_livereload

logger = getLogger("booktracker")
bp = Blueprint("Frontend")
setup_livereload(bp)


@bp.get("/<path:path>")
async def index(request: Request, path: str):
    base: Path = request.app.config.UI_DIR / "public"
    requested_path = base / path
    logger.debug(f"Checking for {requested_path}")
    html = (
        requested_path
        if path and requested_path.exists() and not requested_path.is_dir()
        else base / "index.html"
    )
    return await file(html)
