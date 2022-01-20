from dataclasses import field
from typing import Optional

from booktracker.common.base_model import BaseModel


class Author(BaseModel):
    author_id: int
    eid: str
    name: str
    num_books: Optional[int] = field(default=None)

    class Meta:
        pk_field = "author_id"


class CreateAuthorBody(BaseModel):
    name: str
