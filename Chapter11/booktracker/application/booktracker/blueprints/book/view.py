from logging import getLogger
from typing import Any, Awaitable, Callable, Dict, List, Optional

from asyncpg.exceptions import UniqueViolationError
from booktracker.blueprints.author.executor import AuthorExecutor
from booktracker.blueprints.user.executor import UserExecutor
from booktracker.blueprints.user.model import User
from booktracker.common.csrf import csrf_protected
from booktracker.common.pagination import Pagination
from sanic import Blueprint, Request, json
from sanic.exceptions import NotFound
from sanic.views import HTTPMethodView
from sanic_ext import validate
from sanic_jwt.decorators import inject_user, protected

from .executor import BookExecutor, BookSeriesExecutor
from .hydrator import BookHydrator
from .model import Book, CreateBookBody, CreateSeriesBody, Series

logger = getLogger("booktracker")
bp = Blueprint("Books", url_prefix="/books")


class BookListView(HTTPMethodView, attach=bp):
    @staticmethod
    @validate(json=CreateBookBody)
    @inject_user()
    @protected()
    @csrf_protected
    async def post(request: Request, body: CreateBookBody, user: User):
        book_executor = BookExecutor(request.app.ctx.postgres)
        series_executor = BookSeriesExecutor(request.app.ctx.postgres)
        author_executor = AuthorExecutor(request.app.ctx.postgres)

        if not body.author_is_eid:
            author = await author_executor.create_author(name=body.author)
        else:
            author = await author_executor.get_author_by_eid(eid=body.author)

        if body.series:
            if not body.series_is_eid:
                series = await series_executor.create_book_series(name=body.series)
            else:
                series = await series_executor.get_book_series_by_eid(eid=body.series)

        if not body.title_is_eid:
            book = await book_executor.create_book(
                title=body.title,
                author_id=author.author_id,
                series_id=series.series_id if body.series else None,
            )
        else:
            book = await book_executor.get_book_by_eid(eid=body.title)

        try:
            await book_executor.create_book_to_user(
                book_id=book.book_id, user_id=user.user_id
            )
        except UniqueViolationError:
            ...

        return json({"book": book}, status=201)

    @staticmethod
    @inject_user()
    async def get(
        request: Request,
        pagination: Optional[Pagination] = None,
        user: Optional[User] = None,
    ):
        executor = BookExecutor(request.app.ctx.postgres, BookHydrator())
        kwargs = {**pagination.to_dict()} if pagination else {}
        getter: Callable[..., Awaitable[List[Book]]] = executor.get_all_books

        if title := request.args.get("title"):
            kwargs["title"] = title
            getter = executor.get_books_by_title
        elif user:
            payload = await request.app.ctx.auth.extract_payload(request)
            user_executor = UserExecutor(request.app.ctx.postgres)
            user = await user_executor.get_by_eid(eid=payload["eid"])
            kwargs["user_id"] = user.user_id
            getter = executor.get_all_books_for_user
        try:
            books = await getter(**kwargs)
        except NotFound:
            books = []
        output = [book.to_dict(include_null=False) for book in books]
        return json({"meta": pagination, "books": output})


class BookDetailsView(HTTPMethodView, attach=bp, uri="/<eid>"):
    @staticmethod
    @inject_user()
    async def get(
        request: Request, eid: str, user: Optional[User], executor: BookExecutor
    ):
        # executor = BookExecutor(request.app.ctx.postgres, BookHydrator())
        getter: Callable[..., Awaitable[Book]] = executor.get_book_by_eid
        kwargs: Dict[str, Any] = {"eid": eid}
        if user:
            getter = executor.get_book_by_eid_for_user
            kwargs["user_id"] = user.user_id
        book = await getter(**kwargs)
        return json({"book": book.to_dict(include_null=False)})


class BookLoveView(HTTPMethodView, attach=bp, uri="/<eid>/love"):
    @staticmethod
    @inject_user()
    @protected()
    @csrf_protected
    async def put(request: Request, eid: str, user: User):
        executor = BookExecutor(request.app.ctx.postgres, BookHydrator())
        await executor.update_toggle_book_is_loved(eid=eid, user_id=user.user_id)
        return json({"ok": True})


class BookStateView(HTTPMethodView, attach=bp, uri="/<eid>/state"):
    @staticmethod
    @inject_user()
    @protected()
    @csrf_protected
    async def put(request: Request, eid: str, user: User):
        executor = BookExecutor(request.app.ctx.postgres, BookHydrator())
        await executor.update_book_state(
            eid=eid, user_id=user.user_id, state=request.json["state"]
        )
        return json({"ok": True})


class BookSeriesListView(HTTPMethodView, attach=bp, uri="/series"):
    @staticmethod
    async def get(request: Request, pagination: Pagination):
        executor = BookSeriesExecutor(request.app.ctx.postgres)
        kwargs = {**pagination.to_dict()}
        getter: Callable[..., Awaitable[List[Series]]] = executor.get_all_series

        if name := request.args.get("name"):
            kwargs["name"] = name
            getter = executor.get_series_by_name
        try:
            series = await getter(**kwargs)
        except NotFound:
            series = []

        return json({"meta": pagination, "series": series})

    @staticmethod
    @validate(json=CreateSeriesBody)
    @csrf_protected
    async def post(request: Request, body: CreateSeriesBody):
        executor = BookSeriesExecutor(request.app.ctx.postgres)
        series = await executor.create_book_series(**body.to_dict())
        return json({"series": series}, status=201)
