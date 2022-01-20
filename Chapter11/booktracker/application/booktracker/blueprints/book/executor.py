from typing import List, Optional

from booktracker.blueprints.book.model import Book, Series
from booktracker.common.dao.executor import BaseExecutor
from booktracker.common.eid import generate


class BookExecutor(BaseExecutor):
    async def get_all_books(
        self,
        *,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[Book]:
        query = self._queries["get_all_books"]
        records = await self.db.fetch_all(
            query, {"limit": limit, "offset": offset}
        )
        books = self.hydrator.hydrate(records, Book, True, exclude)

        return books

    async def get_books_by_title(
        self,
        *,
        title: str,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[Book]:
        query = self._queries["get_books_by_title"]
        records = await self.db.fetch_all(
            query, {"limit": limit, "offset": offset, "title": title}
        )
        books = self.hydrator.hydrate(records, Book, True, exclude)

        return books

    async def get_all_books_for_user(
        self,
        *,
        user_id: int,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[Book]:
        query = self._queries["get_all_books_for_user"]
        records = await self.db.fetch_all(
            query, {"limit": limit, "offset": offset, "user_id": user_id}
        )
        books = self.hydrator.hydrate(records, Book, True, exclude)

        return books

    async def create_book(
        self,
        *,
        title: str,
        author_id: int,
        series_id: Optional[int] = None,
        eid: str = "",
    ) -> Book:
        eid = eid or generate(width=24)
        query = self._queries["create_book"]
        record = await self.db.fetch_one(
            query,
            {
                "title": title,
                "author_id": author_id,
                "series_id": series_id,
                "eid": eid,
            },
        )

        values = {"title": title, "eid": eid}
        if record:
            values["book_id"] = record["book_id"]
        book = self.hydrator.hydrate(values, Book, True)

        return book

    async def create_book_to_user(
        self,
        *,
        book_id: int,
        user_id: int,
    ) -> None:
        ...

    async def get_book_by_eid(
        self,
        *,
        eid: str,
    ) -> Book:
        ...

    async def get_book_by_eid_for_user(
        self,
        *,
        eid: str,
        user_id: int,
    ) -> Book:
        ...

    async def update_toggle_book_is_loved(
        self,
        *,
        eid: str,
        user_id: int,
    ) -> None:
        ...

    async def update_book_state(
        self,
        *,
        eid: str,
        user_id: int,
        state: str,
    ) -> None:
        ...


class BookSeriesExecutor(BaseExecutor):
    async def get_all_series(
        self,
        *,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[Series]:
        ...

    async def get_series_by_name(
        self,
        *,
        name: str,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[Series]:
        ...

    async def create_book_series(
        self,
        *,
        name: str,
        eid: str = "",
    ) -> Series:
        ...

    async def get_book_series_by_eid(
        self,
        *,
        eid: str,
    ) -> Series:
        ...
