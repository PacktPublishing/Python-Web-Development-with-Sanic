from typing import Any, List, Literal, Mapping, Optional, Type, TypeVar, Union, overload

from booktracker.common.base_model import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)
RecordT = Mapping[str, Any]
ExcludeT = Optional[List[str]]


class Hydrator:
    """
    Responsible from converting a dict-like object into a model. This will
    mainly be used for converting from DB results to Python objects.
    """

    @overload
    def hydrate(
        self,
        record: RecordT,
        model: Type[ModelT],
        as_list: Literal[False],
        exclude: ExcludeT = None,
    ) -> ModelT:
        ...

    @overload
    def hydrate(
        self,
        record: List[RecordT],
        model: Type[ModelT],
        as_list: Literal[True],
        exclude: ExcludeT = None,
    ) -> List[ModelT]:
        ...

    def hydrate(
        self,
        record: Union[RecordT, List[RecordT]],
        model: Type[ModelT],
        as_list: bool,
        exclude: ExcludeT = None,
    ) -> Union[ModelT, List[ModelT]]:
        if as_list:
            record = [record] if not isinstance(record, list) else record
            return [self.do_hydration(r, model, exclude) for r in record]
        if isinstance(record, list):
            raise TypeError("Unexpectedly found multiple records while hydrating")
        return self.do_hydration(record, model, exclude)

    def do_hydration(
        self,
        record: RecordT,
        model: Type[ModelT],
        exclude: ExcludeT = None,
    ) -> ModelT:
        obj = model(**record)
        if exclude:
            obj.__state__.exclude = exclude
        return obj
