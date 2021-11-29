from sanic import Sanic, text
from sanic.log import logger

app = Sanic(__name__)
app.config.REAL_IP_HEADER = "do-connecting-ip"


@app.get("/")
async def handler(request):
    logger.info(request.headers)
    return text(f"Hello from {request.remote_addr}")


@app.get("/healthz")
async def healthz(request):
    return text("OK")
