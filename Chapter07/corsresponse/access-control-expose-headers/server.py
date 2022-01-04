from sanic import HTTPResponse, Request, Sanic, text

app = Sanic(__name__)
app.config.ALLOWED_ORIGINS = ["http://mysite.com", "http://localhost:8000"]


@app.get("/")
async def handler(request: Request):
    response = text("Hi")
    response.headers["foobar"] = "hello, 123"
    return response


app.static("/test", "./test.html")


def is_preflight(request: Request) -> bool:
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

    response.headers["access-control-allow-origin"] = origin
    # Uncomment this line to show the headers
    # response.headers["access-control-expose-headers"] = "foobar"
