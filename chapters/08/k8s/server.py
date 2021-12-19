from sanic import HTTPResponse, Request, Sanic, text
from sanic.log import logger

app = Sanic(__name__)
app.config.REAL_IP_HEADER = "x-real-ip"


@app.get("/")
async def handler(request: Request) -> HTTPResponse:
    logger.info(request.headers)
    return text(f"Hello from {request.remote_addr}")


@app.get("/healthz")
async def healthz(request: Request) -> HTTPResponse:
    return text("OK")
