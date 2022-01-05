import aiofiles
from sanic import Request, Sanic, text
from sanic.views import stream

app = Sanic(__name__)
app.config.FALLBACK_ERROR_FORMAT = "text"


@app.post("/transaction")
@stream
async def transaction(request: Request):
    result = ""
    while True:
        body = await request.stream.read()  # type: ignore
        if body is None:
            break
        result += body.decode("utf-8")
    return text(result, status=201)


@app.post("/upload")
@stream
async def upload(request: Request):
    filename = await request.stream.read()  # type: ignore
    async with aiofiles.open(filename.decode("utf-8"), mode="w") as f:
        while True:
            body = await request.stream.read()  # type: ignore
            if body is None:
                break
            await f.write(body.decode("utf-8"))
    return text("Done", status=201)
