from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ariadne import ObjectType
from graphql.type import GraphQLResolveInfo

from world.blueprints.languages.executor import LanguageExecutor
from world.common.dao.integrator import BaseIntegrator
from .executor import CityExecutor
from .models import City

if TYPE_CHECKING:
    from world.blueprints.languages.models import Language


class CityIntegrator(BaseIntegrator):
    name = "city"

    def make_query_def(self) -> List[str]:
        return [
            "city(name: String!): City",
            "cities(country: String, limit: Int, offset: Int): [City]",
        ]

    def make_additional_schema(self) -> ObjectType:
        city = ObjectType("City")
        city.set_field("languages", self.resolve_languages)
        return city

    async def query_city(self, _: Any, info: GraphQLResolveInfo, *, name: str) -> City:
        executor = CityExecutor(info.context.app.ctx.postgres)
        return await executor.get_city_by_name(name=name)

    async def query_cities(
        self,
        _: Any,
        info: GraphQLResolveInfo,
        *,
        country: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[City]:
        executor = CityExecutor(info.context.app.ctx.postgres)
        kwargs: Dict[str, Any] = {}
        if limit:
            kwargs["limit"] = limit
        if offset:
            kwargs["offset"] = offset
        if country:
            cities = await executor.get_cities_by_country_code(
                code=country,
                **kwargs,
            )
        else:
            cities = await executor.get_all_cities(**kwargs)
        return cities

    async def resolve_languages(
        self, city: City, info: GraphQLResolveInfo
    ) -> List[Language]:
        executor = LanguageExecutor(info.context.app.ctx.postgres)
        return await executor.get_by_country_code(country_code=city.countrycode)
