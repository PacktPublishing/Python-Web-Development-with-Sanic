from typing import List, Optional

from booktracker.blueprints.user.model import User
from booktracker.common.dao.executor import BaseExecutor


class UserExecutor(BaseExecutor):
    async def get_by_eid(
        self,
        *,
        eid: str,
        exclude: Optional[List[str]] = None,
    ) -> User:
        ...

    async def get_by_login(
        self,
        *,
        login: str,
        exclude: Optional[List[str]] = None,
    ) -> User:
        ...

    async def create_user(
        self,
        *,
        login: str,
        name: Optional[str] = None,
        avatar: Optional[str] = None,
        profile: Optional[str] = None,
        eid: str = "",
    ) -> User:
        ...
