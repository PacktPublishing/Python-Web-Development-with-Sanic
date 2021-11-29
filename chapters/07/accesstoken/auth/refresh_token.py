from secrets import token_urlsafe
from bcrypt import hashpw, gensalt
from .user import User


def generate_token():
    api_key = token_urlsafe()
    hashed_key = hashpw(api_key.encode("utf-8"), gensalt())
    return api_key, hashed_key


async def store_refresh_token(user: User, hased_key: str) -> None:
    user.refresh_hash = hased_key
