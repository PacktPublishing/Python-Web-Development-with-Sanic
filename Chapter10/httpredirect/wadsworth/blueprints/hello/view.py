from sanic import Blueprint, HTTPResponse, Request, json
from sanic.views import HTTPMethodView

bp = Blueprint("Hello", url_prefix="/hello")


class HelloView(HTTPMethodView, attach=bp, uri="/<name>"):
    async def get(self, request: Request, name: str) -> HTTPResponse:
        return json({"hello": name})
