from sanic import Blueprint, text
import random
import asyncio
from hiking.common.cache import cache_response


bp = Blueprint("Slow", url_prefix="/slow")


@bp.get("")
@cache_response("tortoise")
async def wow_super_slow(request):
    wait_time = 0
    for _ in range(10):
        t = random.random()
        await asyncio.sleep(t)
        wait_time += t
    return text(f"Wow, that took {wait_time:.2f}s!")
