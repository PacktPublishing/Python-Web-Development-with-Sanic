from datetime import datetime, timedelta

from bcrypt import checkpw
from sanic import HTTPResponse, Request, Sanic, json, text
from sanic.exceptions import Forbidden

from auth.access_token import (
    check_access_token,
    generate_access_token,
    get_token_from_request,
)
from auth.cookie import set_cookie
from auth.decorator import protected
from auth.refresh_token import generate_token, store_refresh_token
from auth.user import authenticate_login_credentials, get_user_from_request

app = Sanic(__name__)
app.config.JWT_SECRET = "somesecret"
app.config.JWT_EXPIRATION = timedelta(minutes=10)
app.config.REFRESH_EXPIRATION = timedelta(hours=24)
app.config.COOKIE_DOMAIN = "localhost"

app.static("/periodic", "./index-refresh-periodically.html")
app.static("/exception", "./index-refresh-on-exception.html")


@app.get("/")
@protected
async def handler(request: Request) -> HTTPResponse:
    return text(request.ip)


@app.post("/login")
async def login(request: Request) -> HTTPResponse:
    user = await authenticate_login_credentials(
        request.json["username"],
        request.json["password"],
    )
    access_token_exp = datetime.now() + request.app.config.JWT_EXPIRATION
    refresh_token_exp = datetime.now() + request.app.config.REFRESH_EXPIRATION
    access_token = generate_access_token(
        user,
        request.app.config.JWT_SECRET,
        int(access_token_exp.timestamp()),
    )
    refresh_token, hashed_key = generate_token()
    await store_refresh_token(user, hashed_key.decode())

    response = json({"payload": access_token.payload})
    set_cookie(
        response,
        "access_token",
        access_token.header_payload,
        httponly=False,
        domain=request.app.config.COOKIE_DOMAIN,
        exp=access_token_exp,
    )
    set_cookie(
        response,
        "access_token_signature",
        access_token.signature,
        httponly=True,
        domain=request.app.config.COOKIE_DOMAIN,
        exp=access_token_exp,
    )
    set_cookie(
        response,
        "refresh_token",
        refresh_token,
        httponly=True,
        samesite="strict",
        domain=request.app.config.COOKIE_DOMAIN,
        exp=refresh_token_exp,
    )

    return response


@app.post("/refresh")
@protected
async def refresh_access_token(request: Request) -> HTTPResponse:
    user = await get_user_from_request(request)
    access_token = get_token_from_request(request)
    refresh_token = request.cookies["refresh_token"]

    if not user.refresh_hash:
        raise Forbidden("Invalid request")

    is_valid_refresh = checkpw(
        refresh_token.encode("utf-8"),
        user.refresh_hash.encode("utf-8"),
    )
    is_valid_access = check_access_token(
        access_token, request.app.config.JWT_SECRET, allow_expired=True
    )

    if not is_valid_refresh or not is_valid_access:
        raise Forbidden("Invalid request")

    access_token_exp = datetime.now() + request.app.config.JWT_EXPIRATION
    generated_access_token = generate_access_token(
        user,
        request.app.config.JWT_SECRET,
        int(access_token_exp.timestamp()),
    )

    response = json({"payload": generated_access_token.payload})
    set_cookie(
        response,
        "access_token",
        generated_access_token.header_payload,
        httponly=False,
    )
    set_cookie(
        response,
        "access_token_signature",
        generated_access_token.signature,
        httponly=True,
    )

    return response
