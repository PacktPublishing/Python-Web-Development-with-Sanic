from functools import wraps
from typing import Any, Callable, Coroutine, Dict, Union, cast

from aioredis.client import Redis
from sanic import Request
from sanic.response import HTTPResponse, raw

FuncT = Callable[..., Coroutine[None, None, HTTPResponse]]


def make_key(build_key: str, request: Request) -> str:
    return ":".join(["cached-response", build_key, request.name])


async def set_cached_response(
    response: HTTPResponse,
    redis: Redis,
    key: str,
    exp: int,
) -> None:
    await redis.hmset(
        key,
        {
            b"body": response.body or b"",
            b"status": str(response.status).encode("utf-8"),
            b"content_type": (response.content_type or "").encode("utf-8"),
        },
    )
    await redis.expire(key, exp)


async def get_cached_response(
    request: Request, redis: Redis, key: str
) -> Dict[str, Any]:
    exists = await redis.hgetall(key)
    if exists and not request.args.get("refresh"):
        cached_response = {
            k.decode("utf-8"): v.decode("utf-8") for k, v in exists.items()
        }
        cached_response["status"] = int(cached_response["status"])
        return cached_response

    return {}


def cache_response(build_key: str, exp: int = 60 * 60 * 72) -> Callable[[FuncT], FuncT]:
    """
    Cache an expensive response in Redis for quicker retrieval on subsequent
    calls to the endpoint
    """

    def decorator(f: FuncT) -> FuncT:
        @wraps(f)
        async def decorated_function(
            request: Request, *handler_args: Any, **handler_kwargs: Any
        ) -> HTTPResponse:
            cache: Redis = request.app.ctx.redis
            key = make_key(build_key, request)

            if cached_response := await get_cached_response(request, cache, key):
                response = raw(**cached_response)
            else:
                response = await f(request, *handler_args, **handler_kwargs)
                await set_cached_response(response, cache, key, exp)

            return response

        return cast(FuncT, decorated_function)

    return decorator
