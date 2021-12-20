from typing import List, Optional
from world.blueprints.cities.models import City
from world.common.dao.executor import BaseExecutor


class CityExecutor(BaseExecutor):
    async def get_all_cities(
        self,
        *,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[City]:
        ...

    async def get_cities_by_country_code(
        self,
        *,
        code: str,
        exclude: Optional[List[str]] = None,
        limit: int = 15,
        offset: int = 0,
    ) -> List[City]:
        ...

    async def get_city_by_name(
        self, name: str, *, exclude: Optional[List[str]] = None
    ) -> City:
        ...

    async def get_city_by_id(
        self, city_id: int, *, exclude: Optional[List[str]] = None
    ) -> City:
        ...
