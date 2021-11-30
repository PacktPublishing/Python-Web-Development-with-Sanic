from sanic import Sanic, Request, json
from itertools import count


app = Sanic("test")


@app.before_server_start
def setup(app, _):
    app.ctx.counter = count()


@app.get("")
async def handler(request: Request):
    return json(next(request.app.ctx.counter))
