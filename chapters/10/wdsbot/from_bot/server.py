from sanic import Request, Sanic, json

app = Sanic(__name__)


@app.get("/")
async def handler(request: Request):
    await request.app.ctx.general.send("Someone sent a message")
    return json({"foo": "bar"})


@app.before_server_start
async def before_server_start(app, _):
    await app.ctx.general.send("Wadsworth, reporting for duty")
