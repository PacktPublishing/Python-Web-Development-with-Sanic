from datetime import datetime, timedelta
from sanic import Sanic, text, json
from auth.decorator import protected
from auth.user import authenticate_login_credentials, get_user_from_request
from auth.access_token import generate_access_token, check_access_token
from auth.refresh_token import generate_token, store_refresh_token
from auth.cookie import set_cookie
from bcrypt import checkpw
from sanic.exceptions import Forbidden
from sanic.response import empty

app = Sanic(__name__)
app.config.JWT_SECRET = "somesecret"
app.config.JWT_EXPIRATION = timedelta(minutes=10)
app.config.REFRESH_EXPIRATION = timedelta(hours=24)
app.config.COOKIE_DOMAIN = "127.0.0.1"


@app.get("/")
@protected
async def handler(request):
    return text(request.ip)


@app.post("/login")
async def login(request):
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
    refresh_token, hased_key = generate_token()
    await store_refresh_token(user, hased_key)

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
        "access_token",
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
async def refresh_access_token(request):
    print(f"{request.cookies}")
    user = await get_user_from_request(request)
    access_token = request.cookies["access_token"]
    refresh_token = request.cookies["refresh_token"]

    is_valid_refresh = checkpw(
        refresh_token.encode("utf-8"),
        user.refresh_hash,
    )
    is_valid_access = check_access_token(access_token, allow_expired=True)

    if not is_valid_refresh or not is_valid_access:
        return Forbidden("Invalid request")

    access_token = generate_access_token(user)

    response = empty()
    set_cookie(
        response,
        "access_token",
        access_token.header_payload,
        httponly=False,
    )
    set_cookie(
        response,
        "access_token",
        access_token.signature,
        httponly=True,
    )

    return response
