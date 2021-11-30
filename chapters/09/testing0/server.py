from sanic import Sanic, text

app = Sanic(__name__)


@app.get("/")
async def handler(request):
    return text("...")
