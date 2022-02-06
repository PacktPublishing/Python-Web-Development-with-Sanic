from datetime import datetime
from typing import Optional

from sanic import HTTPResponse


def set_cookie(
    response: HTTPResponse,
    key: str,
    value: str,
    httponly: bool = False,
    samesite: str = "lax",
    domain: Optional[str] = None,
    exp: Optional[datetime] = None,
    secure: bool = True,
) -> None:
    response.cookies[key] = value
    response.cookies[key]["httponly"] = httponly
    response.cookies[key]["path"] = "/"
    response.cookies[key]["secure"] = secure
    response.cookies[key]["samesite"] = samesite

    if domain:
        response.cookies[key]["domain"] = domain

    if exp:
        response.cookies[key]["expires"] = exp
