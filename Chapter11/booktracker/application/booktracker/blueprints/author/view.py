from logging import getLogger
from typing import Awaitable, Callable, List

from booktracker.common.csrf import csrf_protected
from booktracker.common.pagination import Pagination
from sanic import Blueprint, Request, json
from sanic.exceptions import NotFound
from sanic.views import HTTPMethodView
from sanic_ext import validate

from .executor import AuthorExecutor
from .model import Author, CreateAuthorBody

bp = Blueprint("Authors", url_prefix="/authors")
logger = getLogger("booktracker")


class AuthorListView(HTTPMethodView, attach=bp):
    @staticmethod
    async def get(request: Request, pagination: Pagination):
        executor = AuthorExecutor(request.app.ctx.postgres)
        kwargs = {**pagination.to_dict()}
        getter: Callable[
            ..., Awaitable[List[Author]]
        ] = executor.get_all_authors

        if name := request.args.get("name"):
            kwargs["name"] = name
            getter = executor.get_authors_by_name

        try:
            authors = await getter(**kwargs)
        except NotFound:
            authors = []

        return json({"meta": pagination, "authors": authors})

    @staticmethod
    @validate(json=CreateAuthorBody)
    @csrf_protected
    async def post(request: Request, body: CreateAuthorBody):
        executor = AuthorExecutor(request.app.ctx.postgres)
        author = await executor.create_author(**body.to_dict())
        return json({"author": author}, status=201)
