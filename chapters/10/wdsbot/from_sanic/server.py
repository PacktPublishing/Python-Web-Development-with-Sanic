import asyncio

from sanic import Request, Sanic, json

from bot import client

app = Sanic(__name__)
app.config.GENERAL_CHANNEL_ID = 9999999999
app.config.DISCORD_TOKEN = "ABCDEFG"


@app.get("/")
async def handler(request: Request):

    await request.app.ctx.general.send("Someone sent a message")
    return json({"foo": "bar"})


@app.before_server_start
async def startup_wadsworth(app, _):
    app.ctx.wadsworth = client
    app.add_task(client.start(app.config.DISCORD_TOKEN))

    while True:
        if client.is_ready():
            app.ctx.general = client.get_channel(app.config.GENERAL_CHANNEL_ID)
            await app.ctx.general.send("Wadsworth, reporting for duty")
            break
        await asyncio.sleep(0.1)


@app.before_server_stop
async def shutdown(app, _):
    await client.close()
