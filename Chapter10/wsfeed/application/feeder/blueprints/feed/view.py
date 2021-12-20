from sanic import Blueprint
from sanic.log import logger
from .channel import Channel

bp = Blueprint("Feed", url_prefix="/feed")


@bp.websocket("/<channel_name>")
async def feed(request, ws, channel_name):
    logger.info("Incoming WS request")
    channel, is_existing = await Channel.get(
        request.app.ctx.pubsub, request.app.ctx.redis, channel_name
    )

    if not is_existing:
        request.app.add_task(channel.receiver())
    client = await channel.register(ws)

    try:
        await client.receiver()
    finally:
        await channel.unregister(client)
