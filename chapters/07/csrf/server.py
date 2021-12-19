from base64 import b64decode, b64encode
from typing import Literal

from sanic import Sanic, text, Request, HTTPResponse
from functools import wraps
from inspect import isawaitable
from sanic.exceptions import Forbidden
from cryptography.fernet import Fernet, InvalidToken
import os

app = Sanic(__name__)
app.config.FALLBACK_ERROR_FORMAT = "text"
app.config.ALLOWED_ORIGINS = ["http://localhost:7777"]
app.config.CSRF_REF_PADDING = 12
app.config.CSRF_REF_LENGTH = 18
# app.config.CSRF_SECRET = Fernet.generate_key()
app.config.CSRF_SECRET = "DZsM9KOs6YAGluhGrEo9oWw4JKTjdiOot9Z4gZ0dGqg="


class CSRFFailure(Forbidden):
    message = "CSRF Failure. Missing or invalid CSRF token."
    quiet = False


def csrf_protected(func):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):

            origin = request.headers.get("origin")
            if request.ctx.from_browser and (
                origin not in app.config.ALLOWED_ORIGINS
                or "browser_check" not in request.cookies
                or not csrf_check(request)
            ):
                raise CSRFFailure

            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response

            return response

        return decorated_function

    return decorator(func)


@app.on_request
async def check_request(request: Request) -> None:
    request.ctx.from_browser = (
        "origin" in request.headers or "browser_check" in request.cookies
    )


@app.on_response
async def mark_browser(_, response: HTTPResponse) -> None:
    response.cookies["browser_check"] = "1"
    response.cookies["browser_check"]["domain"] = "localhost"
    response.cookies["browser_check"]["httponly"] = True


def generate_csrf(secret: str, ref_length: int, padding: int) -> tuple[str, str]:
    cipher = Fernet(secret)
    ref = os.urandom(ref_length)
    pad = os.urandom(padding)
    pretoken = cipher.encrypt(ref)

    return ref.hex(), b64encode(pad + pretoken).decode("utf-8")


def verify_csrf(secret: str, padding: int, ref: str, token: str) -> None:
    if not ref or not token:
        raise InvalidToken("Token is incorrect")

    cipher = Fernet(secret)
    raw = b64decode(token.encode("utf-8"))
    pretoken = raw[padding:]
    encoded_ref = cipher.decrypt(pretoken)

    if ref != encoded_ref.hex():
        raise InvalidToken("Token is incorrect")


def csrf_check(request: Request) -> Literal[True]:
    csrf_header = request.headers.get("x-xsrf-token")
    csrf_cookie = request.cookies.get("csrf_token")
    ref_token = request.cookies.get("ref_token")

    try:
        verify_csrf(
            request.app.config.CSRF_SECRET,
            request.app.config.CSRF_REF_PADDING,
            ref_token,
            csrf_cookie,
        )
    except InvalidToken as e:
        raise CSRFFailure from e

    if csrf_header != csrf_cookie:
        raise CSRFFailure

    return True


@app.on_response
async def inject_csrf_token(request: Request, response: HTTPResponse) -> None:
    response.cookies["myfavorite"] = "chocolatechip"
    response.cookies["myfavorite"]["domain"] = "mydomain.com"
    response.cookies["myfavorite"]["samesite"] = None
    response.cookies["myfavorite"]["secure"] = True

    if "csrf_token" not in request.cookies or "ref_token" not in request.cookies:
        ref, token = generate_csrf(
            request.app.config.CSRF_SECRET,
            request.app.config.CSRF_REF_LENGTH,
            request.app.config.CSRF_REF_PADDING,
        )

        response.cookies["session_token"] = ref
        response.cookies["session_token"]["domain"] = "localhost"
        response.cookies["session_token"]["httponly"] = True
        response.cookies["session_token"]["samesite"] = "lax"
        response.cookies["session_token"]["secure"] = True

        response.cookies["ref_token"] = ref
        response.cookies["ref_token"]["domain"] = "localhost"
        response.cookies["ref_token"]["httponly"] = True
        response.cookies["ref_token"]["samesite"] = "strict"
        response.cookies["ref_token"]["secure"] = True

        response.cookies["csrf_token"] = token
        response.cookies["csrf_token"]["domain"] = "localhost"
        response.cookies["csrf_token"]["samesite"] = "strict"
        response.cookies["csrf_token"]["secure"] = True


@app.post("/")
@csrf_protected
async def handler(request: Request) -> HTTPResponse:
    return text("Hi")


@app.get("/start")
async def handler2(request: Request) -> HTTPResponse:
    return text("Hi")
