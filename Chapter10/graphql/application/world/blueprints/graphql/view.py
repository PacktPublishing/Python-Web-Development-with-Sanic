from typing import Any

from ariadne import graphql, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from sanic import Blueprint, HTTPResponse, Request, Sanic, html, json
from sanic.views import HTTPMethodView

from world.blueprints.cities.integrator import CityIntegrator
from world.blueprints.countries.integrator import CountryIntegrator
from world.blueprints.languages.integrator import LanguageIntegrator
from world.common.dao.integrator import RootIntegrator
from .query import query

bp = Blueprint("GraphQL", url_prefix="/graphql")


class GraphQLView(HTTPMethodView, attach=bp, uri=""):
    async def get(self, request: Request) -> HTTPResponse:
        return html(PLAYGROUND_HTML)

    async def post(self, request: Request) -> HTTPResponse:
        success, result = await graphql(
            request.app.ctx.schema,
            request.json,
            context_value=request,
            debug=request.app.debug,
        )

        status_code = 200 if success else 400
        return json(result, status=status_code)


@bp.before_server_start
async def setup_graphql(app: Sanic, _: Any) -> None:
    integrator = RootIntegrator.create(
        CityIntegrator,
        CountryIntegrator,
        LanguageIntegrator,
        query=query,
    )
    integrator.load()
    integrator.attach_resolvers()
    defs = integrator.generate_query_defs()
    print(defs)
    additional = integrator.generate_additional_schemas()
    app.ctx.schema = make_executable_schema(defs, query, *additional)
