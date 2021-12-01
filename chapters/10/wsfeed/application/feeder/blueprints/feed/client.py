from dataclasses import dataclass, field
from uuid import UUID, uuid4
from aioredis import Redis
from sanic.server.websockets.impl import WebsocketImplProtocol


@dataclass
class Client:
    protocol: WebsocketImplProtocol
    redis: Redis
    channel_name: str
    uid: UUID = field(default_factory=uuid4)

    def __hash__(self) -> int:
        return self.uid.int

    async def receiver(self):
        while True:
            message = await self.protocol.recv()
            if not message:
                break
            await self.redis.publish(self.channel_name, message)

    async def shutdown(self):
        await self.protocol.close()
