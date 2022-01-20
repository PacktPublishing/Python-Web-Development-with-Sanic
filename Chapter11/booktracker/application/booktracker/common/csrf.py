import os
from base64 import b64decode, b64encode
from functools import wraps
from inspect import isawaitable

from booktracker.common.cookie import set_cookie
from cryptography.fernet import Fernet, InvalidToken
from sanic import HTTPResponse, Request, Sanic
from sanic.exceptions import Forbidden


class CSRFFailure(Forbidden):
    message = "CSRF Failure. Missing or invalid CSRF token."
    quiet = False


def csrf_protected(func):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):

            origin = request.headers.get("origin")
            if request.ctx.from_browser and (
                origin not in request.app.config.CORS_ORIGINS
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


def setup_csrf(app: Sanic):
    @app.on_request
    async def check_request(request: Request):
        request.ctx.from_browser = (
            "origin" in request.headers or "browser_check" in request.cookies
        )

    @app.on_response
    async def mark_browser(_, response: HTTPResponse):
        set_cookie(
            response=response, key="browser_check", value="1", httponly=True
        )


def generate_csrf(secret, ref_length, padding):
    cipher = Fernet(secret)
    ref = os.urandom(ref_length)
    pad = os.urandom(padding)
    pretoken = cipher.encrypt(ref)

    return ref.hex(), b64encode(pad + pretoken).decode("utf-8")


def verify_csrf(secret, padding, ref, token):
    if not ref or not token:
        raise InvalidToken("Token is incorrect")

    cipher = Fernet(secret)
    raw = b64decode(token.encode("utf-8"))
    pretoken = raw[padding:]
    encoded_ref = cipher.decrypt(pretoken)

    if ref != encoded_ref.hex():
        raise InvalidToken("Token is incorrect")


def csrf_check(request: Request):
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
