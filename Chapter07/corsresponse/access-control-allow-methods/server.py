from functools import partial

from sanic import Request, Sanic, response, text

app = Sanic(__name__)
app.config.ALLOWED_ORIGINS = [
    "http://mysite.com",
    "http://127.0.0.1:8888",
    "http://127.0.0.1:7777",
]


@app.get("/")
async def handler(request: Request):
    return text("Hi")


def is_preflight(request: Request) -> bool:
    return (
        request.method == "OPTIONS"
        and "access-control-request-method" in request.headers
    )


async def options_handler(request, methods):
    resp = response.empty()
    if request.ctx.preflight:
        resp.headers["access-control-allow-credentials"] = "true"
        resp.headers["access-control-allow-methods"] = ",".join(methods)
    resp.headers["vary"] = "origin"
    origin = request.headers.get("origin")
    if not origin or origin not in request.app.config.ALLOWED_ORIGINS:
        return

    resp.headers["access-control-allow-origin"] = origin
    return resp


@app.on_request
async def check_preflight(request: Request) -> None:
    request.ctx.preflight = is_preflight(request)


@app.before_server_start
def add_info_handlers(app: Sanic, _):
    app.router.reset()
    for group in app.router.groups.values():
        if "OPTIONS" not in group.methods:
            app.add_route(
                handler=partial(options_handler, methods=group.methods),
                uri=group.uri,
                methods=["OPTIONS"],
                strict_slashes=group.strict,
                name="options_handler",
            )
    app.router.finalize()
