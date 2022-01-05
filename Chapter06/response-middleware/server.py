from sanic import Blueprint, Sanic, json

app = Sanic(__name__)

bp = Blueprint("Six", url_prefix="/six")


@bp.on_response
async def complete(request, response):
    return json(request.ctx.numbers)


@app.on_request
async def zero(request):
    request.ctx.numbers = []


@app.on_response
async def one(request, response):
    request.ctx.numbers.append(1)


@bp.on_response
async def two(request, response):
    request.ctx.numbers.append(2)


@app.on_response
async def three(request, response):
    request.ctx.numbers.append(3)


@bp.on_response
async def four(request, response):
    request.ctx.numbers.append(4)


@app.on_response
async def five(request, response):
    request.ctx.numbers.append(5)


@bp.on_response
async def six(request, response):
    request.ctx.numbers.append(6)


@bp.get("/")
async def bp_handler(request):
    request.ctx.numbers = []
    return json("blah blah blah")


app.blueprint(bp)
