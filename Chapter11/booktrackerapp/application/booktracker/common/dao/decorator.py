from functools import wraps
from inspect import getsourcelines, signature
from logging import getLogger
from typing import get_args, get_origin

from booktracker.common.eid import generate
from sanic.exceptions import NotFound, SanicException

logger = getLogger("booktracker")


def execute(func):
    """
    Responsible for executing a DB query and passing the result off to a
    hydrator.

    If the Executor does not contain any code, then the assumption is that
    we should automatically execute the in memory SQL, and passing the results
    off to the base Hydrator.
    """
    sig = signature(func)
    src = getsourcelines(func)

    # TODO
    # - Make sure that this is the ONLY part of the source, and also
    #   accept methods that only have a docstring and no code.
    auto_exec = src[0][-1].strip() in ("...", "pass")
    model = sig.return_annotation
    as_list = False
    is_create = func.__name__.startswith("create_")

    if model is not None and (origin := get_origin(model)):
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
            if is_create and "eid" in sig.parameters.keys():
                kwargs["eid"] = generate(width=24)

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

                if results:
                    if isinstance(results, list):
                        results = list(map(dict, results))
                    else:
                        results = dict(results)

                if model is None:
                    return None

                if not results and not is_create:
                    raise NotFound(f"Did not find {model.__name__}")
                elif not results and is_create:
                    results = values
                elif is_create and len(results) == 1:
                    results.update(values)

                return self.hydrator.hydrate(results, model, as_list, exclude)

            return await f(*args, **kwargs)

        return decorated_function

    return decorator(func)
