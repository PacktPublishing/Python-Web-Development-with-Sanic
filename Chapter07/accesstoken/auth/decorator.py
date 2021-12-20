from inspect import isawaitable
from functools import wraps


def protected(maybe_func=None, *, arg1=None, arg2=None):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):

            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response

            return response

        return decorated_function

    return decorator(maybe_func) if maybe_func else decorator
