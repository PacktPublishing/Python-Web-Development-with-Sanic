from sanic import Blueprint, Request, HTTPResponse, json

bp = Blueprint("Bookv2", url_prefix="/book")


@bp.get("/")
async def get_all_books(request: Request) -> HTTPResponse:
    return json({"books": ["The Adventures of Tom Sawyer", "Treasure Island"]})
