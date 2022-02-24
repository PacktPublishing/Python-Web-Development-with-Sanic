import asyncio
from typing import Any

from nextcord.threads import Thread
from sanic import HTTPResponse, Request, Sanic, json

from bot import client

app = Sanic("WDSApp")
app.config.GENERAL_CHANNEL_ID = 9999999999
app.config.DISCORD_TOKEN = "ABCDEFG"


@app.get("/")
async def handler(request: Request) -> HTTPResponse:

    await request.app.ctx.general.send("Someone sent a message")
    return json({"foo": "bar"})


@app.before_server_start
async def startup_wadsworth(app: Sanic, _: Any) -> None:
    app.ctx.wadsworth = client
    app.add_task(client.start(app.config.DISCORD_TOKEN))

    while True:
        if client.is_ready():
            app.ctx.general = client.get_channel(app.config.GENERAL_CHANNEL_ID)
            if isinstance(app.ctx.general, Thread):
                await app.ctx.general.send("Wadsworth, reporting for duty")
            break
        await asyncio.sleep(0.1)


@app.before_server_stop
async def shutdown(app: Sanic, _: Any) -> None:
    await client.close()
