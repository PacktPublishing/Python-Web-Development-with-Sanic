from typing import List, Optional
from world.blueprints.countries.models import Country
from world.common.dao.executor import BaseExecutor


class CountryExecutor(BaseExecutor):
    async def get_all_countries(
        self,
        *,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[Country]:
        ...

    async def get_country_by_name(
        self, name: str, *, exclude: Optional[List[str]] = None
    ) -> Country:
        ...
