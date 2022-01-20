from __future__ import annotations

from dataclasses import field
from enum import auto
from typing import Optional

from booktracker.blueprints.author.model import Author
from booktracker.blueprints.user.model import User
from booktracker.common.base_model import BaseEnum, BaseModel


class BookState(BaseEnum):
    READ = auto()
    READING = auto()
    UNREAD = auto()


class Book(BaseModel):
    book_id: int
    eid: str
    title: str
    author: Optional[Author] = field(default=None)
    series: Optional[Series] = field(default=None)
    user: Optional[User] = field(default=None)
    is_loved: Optional[bool] = field(default=None)
    state: Optional[BookState] = field(default=None)

    class Meta:
        pk_field = "book_id"


class Series(BaseModel):
    series_id: int
    eid: str
    name: str

    class Meta:
        pk_field = "series_id"


class CreateBookBody(BaseModel):
    title: str
    author: str
    series: Optional[str] = field(default=None)
    title_is_eid: bool = field(default=False)
    author_is_eid: bool = field(default=False)
    series_is_eid: bool = field(default=False)


class CreateSeriesBody(BaseModel):
    name: str
