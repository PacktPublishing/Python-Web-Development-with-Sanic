from datetime import datetime
from typing import Optional


def set_cookie(
    response,
    key,
    value,
    httponly=False,
    samesite="lax",
    domain: Optional[str] = None,
    exp: Optional[datetime] = None,
    secure: bool = True,
):
    response.cookies[key] = value
    response.cookies[key]["httponly"] = httponly
    response.cookies[key]["path"] = "/"
    response.cookies[key]["secure"] = secure
    response.cookies[key]["samesite"] = samesite

    if domain:
        response.cookies[key]["domain"] = domain

    if exp:
        response.cookies[key]["expires"] = exp
