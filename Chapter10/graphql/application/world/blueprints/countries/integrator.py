from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional
from world.common.dao.integrator import BaseIntegrator
from graphql.type import GraphQLResolveInfo
from world.blueprints.countries.models import Country
from world.blueprints.countries.executor import CountryExecutor
from ariadne import ObjectType

from world.blueprints.cities.executor import CityExecutor
from world.blueprints.languages.executor import LanguageExecutor

if TYPE_CHECKING:
    from world.blueprints.cities.models import City
    from world.blueprints.languages.models import Language


class CountryIntegrator(BaseIntegrator):
    name = "country"

    async def resolve_capital(self, country: Country, info: GraphQLResolveInfo) -> City:
        executor = CityExecutor(info.context.app.ctx.postgres)
        return await executor.get_city_by_id(country.capital)

    def make_additional_schema(self):
        country = ObjectType("Country")
        country.set_field("capital", self.resolve_capital)
        country.set_field("languages", self.resolve_languages)
        return country

    def make_query_def(self):
        return [
            "country(name: String!): Country",
            "countries(limit: Int, offset: Int): [Country]",
        ]

    async def query_country(self, _, info: GraphQLResolveInfo, *, name: str) -> Country:
        executor = CountryExecutor(info.context.app.ctx.postgres)
        return await executor.get_country_by_name(name=name)

    async def query_countries(
        self,
        _,
        info: GraphQLResolveInfo,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Country]:
        executor = CountryExecutor(info.context.app.ctx.postgres)
        kwargs = {}
        if limit:
            kwargs["limit"] = limit
        if offset:
            kwargs["offset"] = offset
        cities = await executor.get_all_countries(**kwargs)  # type: ignore
        return cities

    async def resolve_languages(
        self, country: Country, info: GraphQLResolveInfo
    ) -> List[Language]:
        executor = LanguageExecutor(info.context.app.ctx.postgres)
        return await executor.get_by_country_code(country_code=country.code)
