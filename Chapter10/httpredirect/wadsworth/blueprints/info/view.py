from sanic import Blueprint, HTTPResponse, Request, json
from sanic.views import HTTPMethodView

bp = Blueprint("Info", url_prefix="/info")


class InfoView(HTTPMethodView, attach=bp):
    async def get(self, request: Request) -> HTTPResponse:
        return json({"server": request.app.name})
