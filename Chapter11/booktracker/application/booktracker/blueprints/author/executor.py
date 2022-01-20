from typing import List, Optional

from booktracker.blueprints.author.model import Author
from booktracker.common.dao.executor import BaseExecutor


class AuthorExecutor(BaseExecutor):
    async def get_all_authors(
        self,
        *,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[Author]:
        ...

    async def get_authors_by_name(
        self,
        *,
        name: str,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[Author]:
        ...

    async def create_author(
        self,
        *,
        name: Optional[str] = None,
        eid: str = "",
    ) -> Author:
        ...

    async def get_author_by_eid(
        self,
        *,
        eid: str,
    ) -> Author:
        ...
