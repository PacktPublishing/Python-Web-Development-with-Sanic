import nextcord
from sanic.server.async_server import AsyncioServer

from server import app

client = nextcord.Client()


async def runner(app_server: AsyncioServer):
    app.is_running = True
    try:
        await app_server.startup()
        await app_server.before_start()
        await app_server.after_start()
        await app_server.serve_forever()
    finally:
        app.is_running = False
        app.is_stopping = True
        await app_server.before_stop()
        await app_server.close()
        for connection in app_server.connections:
            connection.close_if_idle()
        await app_server.after_stop()
        app.is_stopping = False


@client.event
async def on_ready():
    app.config.GENERAL_CHANNEL_ID = 9999999999
    app.ctx.wadsworth = client
    app.ctx.general = client.get_channel(app.config.GENERAL_CHANNEL_ID)

    if not app.is_running:
        app_server = await app.create_server(
            port=9999, return_asyncio_server=True
        )
        app.ctx.app_server = app_server
        client.loop.create_task(runner(app_server))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


client.run("ABCDEFG")
