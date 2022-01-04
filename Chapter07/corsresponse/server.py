from functools import partial

from sanic import HTTPResponse, Request, Sanic, response, text

app = Sanic(__name__)
app.config.ALLOWED_ORIGINS = [
    "http://mysite.com",
    # "http://localhost:8888",
    # "http://127.0.0.1:8888",
    # "http://127.0.0.1:7777",
]


@app.route("/", methods=["post", "patch", "get"])
async def handler(request: Request) -> HTTPResponse:
    response = text("Hi")
    response.headers["foobar"] = "hello, 123"
    return response


app.static("/test", "./test.html")


async def options_handler(request: Request, methods: list[str]) -> HTTPResponse:
    resp = response.empty()
    if request.ctx.preflight:
        resp.headers["access-control-allow-credentials"] = "true"
        resp.headers["access-control-allow-headers"] = "counting"
        resp.headers["access-control-allow-methods"] = ",".join(methods)
    return resp


@app.before_server_start
def add_info_handlers(app: Sanic, _) -> None:
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


def is_preflight(request: Request) -> bool:
    return (
        request.method == "OPTIONS"
        and "access-control-request-method" in request.headers
    )


@app.on_request
async def check_preflight(request: Request) -> None:
    request.ctx.preflight = is_preflight(request)


@app.on_response
async def add_cors_headers(request: Request, response: HTTPResponse) -> None:
    # Add headers here on all requests

    origin = request.headers.get("origin")
    print(f"{origin}")
    if not origin or origin not in request.app.config.ALLOWED_ORIGINS:
        return

    response.headers["vary"] = "origin"
    response.headers["access-control-allow-origin"] = origin
    # response.headers["access-control-expose-headers"] = "foobar"
