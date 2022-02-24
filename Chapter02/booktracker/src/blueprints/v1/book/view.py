from sanic import Blueprint, Request, HTTPResponse, json

bp = Blueprint("Book", url_prefix="/book")


@bp.get("/")
async def get_all_books(request: Request) -> HTTPResponse:
    return json(["The Adventures of Tom Sawyer", "Treasure Island"])
