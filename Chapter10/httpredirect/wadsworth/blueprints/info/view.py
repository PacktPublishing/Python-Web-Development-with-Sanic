from sanic import Blueprint, json, Request
from sanic.views import HTTPMethodView

bp = Blueprint("Info", url_prefix="/info")


class InfoView(HTTPMethodView, attach=bp):
    async def get(self, request: Request):
        return json({"server": request.app.name})
