from sanic import Blueprint, Request, HTTPResponse, json

bp = Blueprint("Author", url_prefix="/author")


@bp.get("/")
async def get_all_books(request: Request) -> HTTPResponse:
    return json(["Mark Twain", "Robert Louis Stevenson"])
