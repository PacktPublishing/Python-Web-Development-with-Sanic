from sanic import Blueprint, json, Request
from sanic.views import HTTPMethodView

bp = Blueprint("Hello", url_prefix="/hello")


class HelloView(HTTPMethodView, attach=bp, uri="/<name>"):
    async def get(self, request: Request, name: str):
        return json({"hello": name})
