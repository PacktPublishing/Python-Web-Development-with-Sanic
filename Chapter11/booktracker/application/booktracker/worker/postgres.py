from databases import Database
from sanic import Sanic

from booktracker.common.dao.executor import BaseExecutor
from booktracker.common.dao.hydrator import Hydrator

app = Sanic.get_app("BooktrackerApp")


@app.before_server_start
async def setup_postgres(app: Sanic, _) -> None:
    app.ctx.postgres = Database(
        app.config.POSTGRES_DSN,
        min_size=app.config.POSTGRES_MIN,
        max_size=app.config.POSTGRES_MAX,
    )


@app.after_server_start
async def connect_postgres(app: Sanic, _) -> None:
    await app.ctx.postgres.connect()


@app.after_server_start
async def load_sql(app: Sanic, _) -> None:
    BaseExecutor.load(Hydrator())


@app.after_server_stop
async def shutdown_postgres(app: Sanic, _) -> None:
    await app.ctx.postgres.disconnect()
