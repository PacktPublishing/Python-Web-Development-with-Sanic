from sanic import Sanic, text

app = Sanic(__name__)


@app.get("/<name>")
async def handler(request, name):
    return text(f"Hi {name}")


# DO NOT DO THIS
# @app.on_response
# async def cors(_, resp):
#     resp.headers["Access-Control-Allow-Origin"] = "*"
