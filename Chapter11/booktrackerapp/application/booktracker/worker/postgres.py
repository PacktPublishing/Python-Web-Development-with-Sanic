from booktracker.common.dao.executor import BaseExecutor
from booktracker.common.dao.hydrator import Hydrator
from databases import Database
from sanic import Sanic

app = Sanic.get_app("BooktrackerApp")


@app.before_server_start
async def setup_postgres(app, _):
    app.ctx.postgres = Database(
        app.config.POSTGRES_DSN,
        min_size=app.config.POSTGRES_MIN,
        max_size=app.config.POSTGRES_MAX,
    )


@app.after_server_start
async def connect_postgres(app, _):
    await app.ctx.postgres.connect()


@app.after_server_start
async def load_sql(app, _):
    BaseExecutor.load(Hydrator())


@app.after_server_stop
async def shutdown_postgres(app, _):
    await app.ctx.postgres.disconnect()
