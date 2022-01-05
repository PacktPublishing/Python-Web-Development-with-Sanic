from sanic import Blueprint, Sanic, json

app = Sanic(__name__)


bp = Blueprint("Six", url_prefix="/six")


@app.on_request
async def one(request):
    request.ctx.numbers = []
    request.ctx.numbers.append(1)


@bp.on_request
async def two(request):
    request.ctx.numbers.append(2)


@app.on_request
async def three(request):
    request.ctx.numbers.append(3)


@bp.on_request
async def four(request):
    request.ctx.numbers.append(4)


@app.on_request
async def five(request):
    request.ctx.numbers.append(5)


@bp.on_request
async def six(request):
    request.ctx.numbers.append(6)


@app.get("/")
async def app_handler(request):
    return json(request.ctx.numbers)


@bp.get("/")
async def bp_handler(request):
    return json(request.ctx.numbers)


app.blueprint(bp)
