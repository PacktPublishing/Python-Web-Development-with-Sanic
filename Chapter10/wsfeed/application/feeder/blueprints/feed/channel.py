from __future__ import annotations

from asyncio import Lock
from typing import Set, Tuple

from aioredis import Redis
from aioredis.client import PubSub
from aioredis.exceptions import PubSubError
from sanic.log import logger
from sanic.server.websockets.impl import WebsocketImplProtocol

from .client import Client


class ChannelCache(dict):
    ...


class Channel:
    cache = ChannelCache()

    def __init__(self, pubsub: PubSub, redis: Redis, name: str) -> None:
        self.pubsub = pubsub
        self.redis = redis
        self.name = name
        self.clients: Set[Client] = set()
        self.lock = Lock()

    @classmethod
    async def get(cls, pubsub: PubSub, redis: Redis, name: str) -> Tuple[Channel, bool]:
        is_existing = False

        if name in cls.cache:
            channel = cls.cache[name]
            await channel.acquire_lock()
            is_existing = True
        else:
            channel = cls(pubsub=pubsub, redis=redis, name=name)
            await channel.acquire_lock()

            cls.cache[name] = channel

            await pubsub.subscribe(name)

        return channel, is_existing

    async def acquire_lock(self) -> None:
        if not self.lock.locked():
            logger.debug("Lock acquired")
            await self.lock.acquire()
        else:
            logger.debug("Lock already acquired")

    async def receiver(self) -> None:
        logger.debug(f"Starting PubSub receiver for {self.name}")
        while True:
            try:
                raw = await self.pubsub.get_message(ignore_subscribe_messages=True)
            except PubSubError:
                logger.error(f"PUBSUB closed <{self.name}>", exc_info=True)
                break
            else:
                if raw:
                    logger.debug(f"PUBSUB rcvd <{self.name}>: length=={len(raw)}")
                    for client in self.clients:
                        logger.debug(f"Sending to: {client.uid}")
                        await client.protocol.send(raw["data"])

    async def register(self, protocol: WebsocketImplProtocol) -> Client:
        client = Client(protocol=protocol, redis=self.redis, channel_name=self.name)
        self.clients.add(client)
        await self.publish(f"Client {client.uid} has joined")
        return client

    async def unregister(self, client: Client) -> None:
        if client in self.clients:
            await client.shutdown()
            self.clients.remove(client)

            await self.publish(f"Client {client.uid} has left")

        if not self.clients:
            self.lock.release()
            await self.destroy()

    async def destroy(self) -> None:
        if not self.lock.locked():
            logger.debug(f"Destroying Channel {self.name}")
            await self.pubsub.reset()
            del self.__class__.cache[self.name]
        else:
            logger.debug(f"Abort destroying Channel {self.name}. It is locked")

    async def publish(self, message: str) -> None:
        logger.debug(f"Sending message: {message}")
        await self.redis.publish(self.name, message)
