from __future__ import annotations

from functools import wraps
from inspect import getsourcelines, signature
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    List,
    Mapping,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

from sanic.exceptions import NotFound, SanicException
from world.common.base_model import BaseModel

if TYPE_CHECKING:
    from world.common.dao.executor import BaseExecutor

ModelT = TypeVar("ModelT", bound=BaseModel)
FuncT = Callable[..., Coroutine[None, None, Union[ModelT, List[ModelT]]]]
RecordT = Mapping[str, Any]
ExcludeT = Optional[List[str]]


def execute(func: FuncT[ModelT]) -> FuncT[ModelT]:
    sig = signature(func)
    src = getsourcelines(func)
    auto_exec = src[0][-1].strip() in ("...", "pass")
    model: Type[ModelT] = sig.return_annotation
    as_list: bool = False

    if origin := get_origin(model):
        as_list = bool(origin is list)
        if not as_list:
            raise SanicException(
                f"{func} must return either a model or a list of models. "
                "eg. -> Foo or List[Foo]"
            )
        model = get_args(model)[0]

    name = func.__name__

    def decorator(f: FuncT[ModelT]) -> FuncT[ModelT]:
        @wraps(f)
        async def decorated_function(
            *args: Any, **kwargs: Any
        ) -> Union[ModelT, List[ModelT]]:
            if auto_exec:
                self: BaseExecutor = args[0]
                query = self._queries[name]
                method_name = "fetch_all" if as_list else "fetch_one"
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                values = {**bound.arguments}
                values.pop("self")
                exclude: ExcludeT = values.pop("exclude", None)
                results: Union[RecordT, List[RecordT]] = await getattr(
                    self.db, method_name
                )(query=query, values=values)

                if not results:
                    raise NotFound(f"Did not find {model.__name__}")
                return self.hydrator.hydrate(results, model, as_list, exclude)

            return await f(*args, **kwargs)

        return cast(FuncT[ModelT], decorated_function)

    return decorator(func)
