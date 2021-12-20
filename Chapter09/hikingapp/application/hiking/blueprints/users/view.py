from sanic import Blueprint, json, Request
from sanic.views import HTTPMethodView
from .executor import UserExecutor
from ..hikes.executor import HikeExecutor
from ..hikes.hydrator import HikeHydrator

bp = Blueprint("Users", url_prefix="/users")


class UserListView(HTTPMethodView, attach=bp):
    async def get(self, request: Request):
        executor = UserExecutor(request.app.ctx.postgres)
        users = await executor.get_all_users(exclude=["total_distance_hiked"])
        return json({"users": users})


class UserDetailView(HTTPMethodView, attach=bp, uri="/<name>"):
    async def get(self, request: Request, name: str):
        executor = UserExecutor(request.app.ctx.postgres)
        user = await executor.get_user_by_name(name)
        return json({"user": user})


class UserHikeDetailsView(HTTPMethodView, attach=bp, uri="/<name>/hikes"):
    async def get(self, request: Request, name: str):
        user_executor = UserExecutor(request.app.ctx.postgres)
        hike_executor = HikeExecutor(request.app.ctx.postgres, HikeHydrator())
        user = await user_executor.get_user_by_name(name)
        hikes = await hike_executor.get_hikes_by_user(user)
        return json({"user": user, "hikes": hikes})


class UserHikeDetailsViewV2(HTTPMethodView, attach=bp, uri="/<name>/hikes", version=2):
    async def get(self, request: Request, name: str):
        hike_executor = HikeExecutor(request.app.ctx.postgres, HikeHydrator())
        hikes = await hike_executor.get_hikes_by_user_by_name(name)
        return json({"user": {"name": name.title()}, "hikes": hikes})
