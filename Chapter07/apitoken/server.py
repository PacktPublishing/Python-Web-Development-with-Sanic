from sanic import Sanic, text
from secrets import token_urlsafe
from bcrypt import hashpw, gensalt, checkpw

app = Sanic(__name__)


@app.post("/generate")
async def gen_handler(request):
    api_key, hased_key = generate_token()
    print(api_key, hased_key)
    return text(request.ip)


@app.get("/protected")
async def protected_handler(request):
    token = request.token
    print(
        checkpw(
            token.encode("utf-8"),
            b"$2b$12$bFyir57aGMHsQs95OJzmL.gIHH7n98n6goREdG0j24EnMucn7bR4K",
        )
    )
    return text("hi")


def generate_token():
    api_key = token_urlsafe()
    hashed_key = hashpw(api_key.encode("utf-8"), gensalt())
    return api_key, hashed_key
