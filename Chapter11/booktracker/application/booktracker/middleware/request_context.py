from contextvars import ContextVar

from sanic import Request, Sanic

app = Sanic.get_app("BooktrackerApp")


@app.after_server_start
async def setup_request_context(app, _):
    app.ctx.request = ContextVar("request")


@app.on_request
async def attach_request(request: Request):
    request.app.ctx.request.set(request)
