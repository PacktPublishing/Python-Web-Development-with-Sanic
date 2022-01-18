from sanic import Blueprint, HTTPResponse, Request, response
from sanic.constants import HTTP_METHODS

bp = Blueprint("Redirect")


@bp.route("/<path:path>", methods=HTTP_METHODS, name="redirection_proxy")
async def proxy(request: Request, path: str) -> HTTPResponse:
    return response.redirect(
        request.app.url_for(
            "Redirect.redirection_proxy",
            path=path,
            _server=request.app.ctx.main_app.config.SERVER_NAME,
            _external=True,
            _scheme="https",
        ),
        status=301,
    )
