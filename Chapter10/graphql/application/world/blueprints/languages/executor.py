from typing import List, Optional

from world.blueprints.languages.models import Language
from world.common.dao.executor import BaseExecutor


class LanguageExecutor(BaseExecutor):
    async def get_by_country_code(
        self,
        *,
        country_code: str,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[Language]:
        ...
