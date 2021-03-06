from typing import Any

from databases import Database
from sanic import Sanic

from world.common.dao.executor import BaseExecutor
from world.common.dao.hydrator import Hydrator

app = Sanic.get_app()


@app.before_server_start
async def setup_postgres(app: Sanic, _: Any) -> None:
    app.ctx.postgres = Database(
        app.config.POSTGRES_DSN,
        min_size=app.config.POSTGRES_MIN,
        max_size=app.config.POSTGRES_MAX,
    )


@app.after_server_start
async def connect_postgres(app: Sanic, _: Any) -> None:
    await app.ctx.postgres.connect()


@app.after_server_start
async def load_sql(app: Sanic, _: Any) -> None:
    BaseExecutor.load(Hydrator())


@app.after_server_stop
async def shutdown_postgres(app: Sanic, _: Any) -> None:
    await app.ctx.postgres.disconnect()
