from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional
from world.common.dao.integrator import BaseIntegrator
from graphql.type import GraphQLResolveInfo
from .models import City
from .executor import CityExecutor
from world.blueprints.languages.executor import LanguageExecutor
from ariadne import ObjectType

if TYPE_CHECKING:
    from world.blueprints.languages.models import Language


class CityIntegrator(BaseIntegrator):
    name = "city"

    def make_query_def(self):
        return [
            "city(name: String!): City",
            "cities(country: String, limit: Int, offset: Int): [City]",
        ]

    def make_additional_schema(self):
        city = ObjectType("City")
        city.set_field("languages", self.resolve_languages)
        return city

    async def query_city(self, _, info: GraphQLResolveInfo, *, name: str) -> City:
        executor = CityExecutor(info.context.app.ctx.postgres)
        return await executor.get_city_by_name(name=name)

    async def query_cities(
        self,
        _,
        info: GraphQLResolveInfo,
        *,
        country: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[City]:
        executor = CityExecutor(info.context.app.ctx.postgres)
        kwargs = {}
        if limit:
            kwargs["limit"] = limit
        if offset:
            kwargs["offset"] = offset
        if country:
            cities = await executor.get_cities_by_country_code(
                code=country,
                **kwargs,  # type: ignore
            )
        else:
            cities = await executor.get_all_cities(**kwargs)  # type: ignore
        return cities

    async def resolve_languages(
        self, city: City, info: GraphQLResolveInfo
    ) -> List[Language]:
        executor = LanguageExecutor(info.context.app.ctx.postgres)
        return await executor.get_by_country_code(country_code=city.countrycode)
