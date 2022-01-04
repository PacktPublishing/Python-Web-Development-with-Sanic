from dataclasses import dataclass
from typing import Any, Dict

import jwt
from sanic import Request
from sanic.log import error_logger

from .user import User


@dataclass
class AccessToken:
    payload: Dict[str, Any]
    token: str

    def __str__(self) -> str:
        return self.token

    @property
    def header_payload(self):
        return self._parts[0]

    @property
    def signature(self):
        return self._parts[1]

    @property
    def _parts(self):
        return self.token.rsplit(".", maxsplit=1)


def generate_access_token(user: User, secret: str, exp: int) -> AccessToken:
    payload = {
        "whatever": "youwant",
        "exp": exp,
    }
    raw_token = jwt.encode(payload, secret, algorithm="HS256")
    access_token = AccessToken(payload, raw_token)
    return access_token


def check_access_token(
    access_token: str, secret: str, allow_expired: bool = False
) -> bool:
    try:
        jwt.decode(
            access_token,
            secret,
            algorithms=["HS256"],
            require=["exp"],
            verify_exp=(not allow_expired),
        )
    except jwt.exceptions.InvalidTokenError as e:
        error_logger.exception(e)
        return False

    return True


def get_token_from_request(request: Request) -> str:
    access_token = request.cookies.get("access_token", "")
    access_token_signature = request.cookies.get("access_token_signature", "")
    token = ".".join([access_token, access_token_signature])
    return token
