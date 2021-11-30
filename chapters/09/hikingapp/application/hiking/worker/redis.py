from sanic import Sanic
import aioredis

app = Sanic.get_app()


@app.before_server_start
async def setup_redis(app, _):
    app.ctx.redis_pool = aioredis.BlockingConnectionPool.from_url(
        app.config.REDIS_DSN, max_connections=app.config.REDIS_MAX
    )
    app.ctx.redis = aioredis.Redis(connection_pool=app.ctx.redis_pool)


@app.after_server_stop
async def shutdown_redis(app, _):
    await app.ctx.redis_pool.disconnect()
