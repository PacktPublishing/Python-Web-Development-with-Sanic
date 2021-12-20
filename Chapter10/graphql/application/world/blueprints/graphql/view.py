from sanic import Blueprint, Request, html, json
from sanic.views import HTTPMethodView
from ariadne.constants import PLAYGROUND_HTML
from .query import query
from ariadne import graphql, make_executable_schema
from world.common.dao.integrator import RootIntegrator
from world.blueprints.cities.integrator import CityIntegrator
from world.blueprints.countries.integrator import CountryIntegrator
from world.blueprints.languages.integrator import LanguageIntegrator

bp = Blueprint("GraphQL", url_prefix="/graphql")


class GraphQLView(HTTPMethodView, attach=bp, uri=""):
    async def get(self, request: Request):
        return html(PLAYGROUND_HTML)

    async def post(self, request: Request):
        success, result = await graphql(
            request.app.ctx.schema,
            request.json,
            context_value=request,
            debug=request.app.debug,
        )

        status_code = 200 if success else 400
        return json(result, status=status_code)


@bp.before_server_start
async def setup_graphql(app, _):
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
