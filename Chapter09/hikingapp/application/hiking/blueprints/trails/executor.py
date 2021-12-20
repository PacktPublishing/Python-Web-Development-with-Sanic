from typing import List, Optional
from hiking.blueprints.trails.models import Trail
from hiking.common.dao.executor import BaseExecutor


class TrailExecutor(BaseExecutor):
    async def get_all_trails(
        self, *, exclude: Optional[List[str]] = None
    ) -> List[Trail]:
        ...

    async def get_trail_by_name(
        self, name: str, *, exclude: Optional[List[str]] = None
    ) -> Trail:
        ...
