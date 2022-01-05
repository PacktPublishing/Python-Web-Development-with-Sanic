from typing import Any, List, Literal, Mapping, Optional, Type, TypeVar, Union, overload
from hiking.common.base_model import BaseModel

Model = TypeVar("Model", bound=BaseModel)
RecordT = Mapping[str, Any]
ExcludeT = Optional[List[str]]


class Hydrator:
    @overload
    def hydrate(
        self,
        record: RecordT,
        model: Type[Model],
        as_list: Literal[False],
        exclude: ExcludeT = None,
    ) -> Model:
        ...

    @overload
    def hydrate(
        self,
        record: List[RecordT],
        model: Type[Model],
        as_list: Literal[True],
        exclude: ExcludeT = None,
    ) -> List[Model]:
        ...

    def hydrate(
        self,
        record: Union[RecordT, List[RecordT]],
        model: Type[Model],
        as_list: bool,
        exclude: ExcludeT = None,
    ) -> Union[Model, List[Model]]:

        if as_list:
            record = [record] if not isinstance(record, list) else record
            return [self.do_hydration(r, model, exclude) for r in record]
        if isinstance(record, list):
            raise TypeError("Unexpectedly found multiple records while hydrating")
        return self.do_hydration(record, model, exclude)

    def do_hydration(
        self,
        record: RecordT,
        model: Type[Model],
        exclude: ExcludeT = None,
    ) -> Model:
        obj = model(**record)
        if exclude:
            obj.__state__.exclude = exclude
        return obj
