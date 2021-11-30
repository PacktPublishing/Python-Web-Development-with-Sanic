from sanic import Blueprint, json, Request
from sanic.views import HTTPMethodView
from .executor import TrailExecutor

bp = Blueprint("Trails", url_prefix="/trails")


class TrailListView(HTTPMethodView, attach=bp):
    async def get(self, request: Request):
        executor = TrailExecutor(request.app.ctx.postgres)
        trails = await executor.get_all_trails()
        return json({"trails": trails})


class TrailDetailView(HTTPMethodView, attach=bp, uri="/<name>"):
    async def get(self, request: Request, name: str):
        executor = TrailExecutor(request.app.ctx.postgres)
        trail = await executor.get_trail_by_name(name)
        return json({"trail": trail})
