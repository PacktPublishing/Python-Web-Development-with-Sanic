from sanic import Sanic
from .some_db_connection import FakeDBConnection

app = Sanic.get_app()


@app.before_server_start
async def setup_db_connection(app, _):
    app.ctx.db = FakeDBConnection()
