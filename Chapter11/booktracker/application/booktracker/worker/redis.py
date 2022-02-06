from typing import Any

import aioredis
from sanic import Sanic

app = Sanic.get_app("BooktrackerApp")


@app.before_server_start
async def setup_redis(app: Sanic, _: Any) -> None:
    app.ctx.redis_pool = aioredis.BlockingConnectionPool.from_url(
        app.config.REDIS_DSN, max_connections=app.config.REDIS_MAX
    )
    app.ctx.redis = aioredis.Redis(connection_pool=app.ctx.redis_pool)


@app.after_server_stop
async def shutdown_redis(app: Sanic, _: Any) -> None:
    await app.ctx.redis_pool.disconnect()
