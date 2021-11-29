from http.client import responses
from sanic import Sanic, text, HTTPResponse, Request
from sanic import response

app = Sanic(__name__)
app.config.ALLOWED_ORIGINS = ["http://127.0.0.1:8888", "http://127.0.0.1:7777"]


@app.get("/")
async def handler(request):
    response = text("Hi")
    response.headers["foobar"] = "hello, 123"
    return response


app.static("/test", "./test.html")


async def options_handler(request):
    return response.empty()


@app.before_server_start
def add_info_handlers(app: Sanic, _):
    app.router.reset()
    for group in app.router.groups.values():
        if "OPTIONS" not in group.methods:
            app.add_route(
                handler=options_handler,
                uri=group.uri,
                methods=["OPTIONS"],
                strict_slashes=group.strict,
            )
    app.router.finalize()


def is_preflight(request: Request):
    return (
        request.method == "OPTIONS"
        and "access-control-request-method" in request.headers
    )


@app.on_response
async def add_cors_headers(request: Request, response: HTTPResponse) -> None:
    # Add headers here on all requests

    origin = request.headers.get("origin")
    if not origin or origin not in request.app.config.ALLOWED_ORIGINS:
        return

    response.headers["vary"] = "origin"
    response.headers["access-control-allow-origin"] = origin
    response.headers["access-control-expose-headers"] = "foobar"
    # response.headers["access-control-max-age"] = 60 * 10

    if is_preflight(request):
        response.headers["access-control-allow-credentials"] = "true"
    response.headers["access-control-allow-headers"] = "preflight"
    # response.headers["access-control-allow-methods"] = "options,post"
