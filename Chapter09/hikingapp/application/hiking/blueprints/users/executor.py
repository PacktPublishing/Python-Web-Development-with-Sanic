from typing import List, Optional
from hiking.blueprints.users.models import User
from hiking.common.dao.executor import BaseExecutor


class UserExecutor(BaseExecutor):
    async def get_all_users(self, *, exclude: Optional[List[str]] = None) -> List[User]:
        ...

    async def get_user_by_name(
        self, name: str, *, exclude: Optional[List[str]] = None
    ) -> User:
        ...
