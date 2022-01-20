from logging import getLogger
from typing import Any, Dict

import httpx
from aioredis import Redis
from booktracker.blueprints.user.executor import UserExecutor
from sanic import Request
from sanic.exceptions import NotFound, Unauthorized

from .model import RefreshTokenKey

logger = getLogger("booktracker")


async def authenticate(request: Request):
    """
    Perform authentication handling by taking a GitHub authorization code
    and exchanging it for a GitHub access_token.

    If the user does not exist, we will create them. Since we are relying upon
    GitHub authentication and no other, there is no need to differentiate
    between registration and login. The same flow can be used, and therefore
    once a user is authenticated, we add them to the DB if they do not already
    exist as a user.
    """
    invalid = Unauthorized("Missing or invalid authorization code")
    auth_header = request.headers.get("authorization", "")

    if not auth_header or not auth_header.lower().startswith("code"):
        raise invalid

    _, code = auth_header.split(" ")

    # Exchange the authorization code for an access token
    async with httpx.AsyncClient() as session:
        response = await session.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": request.app.config.GITHUB_OAUTH_CLIENT_ID,
                "client_secret": request.app.config.GITHUB_OAUTH_SECRET,
                "code": code,
            },
            headers={"accept": "application/json"},
        )

    if b"error" in response.content or response.status_code != 200:
        logger.error(response.content)
        raise invalid

    # Access the user's basic profile information from GitHub.
    # What we are mainly after here is the GitHub login ID so we can check
    # if they exist in our system or not.
    async with httpx.AsyncClient() as session:
        response = await session.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {response.json()['access_token']}"
            },
        )

    if b"error" in response.content or response.status_code != 200:
        logger.error(response.content)
        raise invalid

    data = response.json()
    executor = UserExecutor(request.app.ctx.postgres)
    try:
        user = await executor.get_by_login(login=data["login"])
        logger.info(f"Found existing user: {user=}")
    except NotFound:
        user = await executor.create_user(
            login=data["login"],
            name=data["name"],
            avatar=data["avatar_url"],
            profile=data["html_url"],
        )
        logger.info(f"Created new user: {user=}")

    return user


async def retrieve_user(request: Request, payload: Dict[str, Any]):
    if not payload:
        return None

    executor = UserExecutor(request.app.ctx.postgres)
    return await executor.get_by_eid(eid=payload["eid"])


async def payload_extender(payload, user):
    payload.update({"user": user.to_dict()})
    return payload


async def store_refresh_token(user_id, refresh_token, request):
    """The actual keyword argument being passed is `user_id`, but the
    value that it is retrieving is the eid"""
    key = RefreshTokenKey(user_id)
    redis: Redis = request.app.ctx.redis
    await redis.set(str(key), refresh_token)


async def retrieve_refresh_token(request, user_id):
    key = RefreshTokenKey(user_id)
    redis: Redis = request.app.ctx.redis
    return await redis.get(str(key))
