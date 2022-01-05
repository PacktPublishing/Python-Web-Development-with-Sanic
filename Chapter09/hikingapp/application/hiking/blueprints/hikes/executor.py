from typing import List
from hiking.common.dao.executor import BaseExecutor
from .models import Hike

from hiking.blueprints.users.models import User


class HikeExecutor(BaseExecutor):
    async def get_hikes_by_user(self, user: User) -> List[Hike]:
        query = self._queries["get_hikes_by_user"]
        records = await self.db.fetch_all(query, values={"user_id": user.user_id})
        hikes = self.hydrator.hydrate(records, Hike, True)

        return hikes

    async def get_hikes_by_user_by_name(self, name: str) -> List[Hike]:
        ...
