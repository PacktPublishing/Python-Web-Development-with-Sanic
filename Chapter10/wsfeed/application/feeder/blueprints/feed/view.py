from sanic import Blueprint, Request
from sanic.log import logger
from sanic.server.websockets.impl import WebsocketImplProtocol

from .channel import Channel

bp = Blueprint("Feed", url_prefix="/feed")


@bp.websocket("/<channel_name>")
async def feed(request: Request, ws: WebsocketImplProtocol, channel_name: str) -> None:
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
