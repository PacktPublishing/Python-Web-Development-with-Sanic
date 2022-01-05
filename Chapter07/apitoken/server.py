from functools import wraps
from inspect import isawaitable
from secrets import token_urlsafe

from bcrypt import checkpw, gensalt, hashpw
from sanic import Request, Sanic, json, text
from sanic.exceptions import Unauthorized

app = Sanic(__name__)
app.ctx.global_store = b""


def api_key_required(
    maybe_func=None,
    *,
    exception=Unauthorized,
    message="Invalid or unknown API key",
):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            try:
                is_valid = checkpw(
                    request.token.encode("utf-8"), request.app.ctx.global_store
                )

                if not is_valid:
                    raise ValueError("Bad token")
            except ValueError as e:
                raise exception(message) from e

            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response

            return response

        return decorated_function

    return decorator(maybe_func) if maybe_func else decorator


@app.post("/apikey")
async def gen_handler(request: Request):
    api_key, hashed_key = generate_token()
    request.app.ctx.global_store = hashed_key
    print(f"{api_key=}")
    print(f"{hashed_key=}")
    return json({"api_key": api_key})


@app.get("/protected")
@api_key_required
async def protected_handler(request):
    return text("hi")


def generate_token():
    api_key = token_urlsafe()
    hashed_key = hashpw(api_key.encode("utf-8"), gensalt())
    return api_key, hashed_key
