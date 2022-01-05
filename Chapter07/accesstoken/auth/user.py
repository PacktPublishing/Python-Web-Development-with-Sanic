from dataclasses import dataclass, field
from typing import Optional

from sanic import Request


@dataclass
class User:
    user_id: int
    refresh_hash: Optional[str] = field(default=None)


fake_database = {
    1: User(1),
}


async def authenticate_login_credentials(username: str, password: str) -> User:
    # Do some fancy logic to validate the username and password
    return fake_database[1]


async def get_user_from_request(request: Request) -> User:
    return fake_database[1]
