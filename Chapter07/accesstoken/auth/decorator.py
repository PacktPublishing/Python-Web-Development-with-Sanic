from functools import wraps
from inspect import isawaitable

from sanic import Request
from sanic.exceptions import Unauthorized

from auth.access_token import check_access_token, get_token_from_request


def protected(maybe_func=None, *, arg1=None, arg2=None):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            token = get_token_from_request(request)
            if not check_access_token(token, request.app.config.JWT_SECRET):
                raise Unauthorized("Unauthorized access")

            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response

            return response

        return decorated_function

    return decorator(maybe_func) if maybe_func else decorator
