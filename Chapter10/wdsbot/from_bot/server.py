from typing import Any

from sanic import HTTPResponse, Request, Sanic, json

app = Sanic("WDSApp")


@app.get("/")
async def handler(request: Request) -> HTTPResponse:
    await request.app.ctx.general.send("Someone sent a message")
    return json({"foo": "bar"})


@app.before_server_start
async def before_server_start(app: Sanic, _: Any) -> None:
    await app.ctx.general.send("Wadsworth, reporting for duty")
