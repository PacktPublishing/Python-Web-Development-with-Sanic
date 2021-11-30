from inspect import getsource, getsourcelines, isclass, signature
from functools import wraps
from typing import List, get_origin, get_args
from sanic.exceptions import SanicException, NotFound


def execute(func):
    sig = signature(func)
    src = getsourcelines(func)
    auto_exec = src[0][-1].strip() in ("...", "pass")
    model = sig.return_annotation
    as_list = False

    if origin := get_origin(model):
        as_list = bool(origin is list)
        if not as_list:
            return SanicException(
                f"{func} must return either a model or a list of models. "
                "eg. -> Foo or List[Foo]"
            )
        model = get_args(model)[0]

    name = func.__name__

    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            if auto_exec:
                self = args[0]
                query = self._queries[name]
                method_name = "fetch_all" if as_list else "fetch_one"
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                values = {**bound.arguments}
                values.pop("self")
                exclude = values.pop("exclude", None)
                results = await getattr(self.db, method_name)(
                    query=query, values=values
                )

                if not results:
                    raise NotFound(f"Did not find {model.__name__}")
                return self.hydrator.hydrate(results, model, as_list, exclude)

            return await f(*args, **kwargs)

        return decorated_function

    return decorator(func)
