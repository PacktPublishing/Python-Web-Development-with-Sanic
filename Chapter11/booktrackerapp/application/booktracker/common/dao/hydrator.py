from typing import Any, List, Mapping, Optional, Type, Union

from booktracker.common.base_model import BaseModel


class Hydrator:
    """
    Responsible from converting a dict-like object into a model. This will
    mainly be used for converting from DB results to Python objects.
    """

    def hydrate(
        self,
        record: Union[Mapping[str, Any], List[Mapping[str, Any]]],
        model: Type[BaseModel],
        as_list: bool,
        exclude: Optional[List[str]] = None,
    ):
        if as_list and isinstance(record, list):
            return [self.do_hydration(r, model, exclude) for r in record]
        if isinstance(record, list):
            raise TypeError(
                "Unexpectedly found multiple records while hydrating"
            )
        return self.do_hydration(record, model, exclude)

    def do_hydration(
        self,
        record: Mapping[str, Any],
        model: Type[BaseModel],
        exclude: Optional[List[str]] = None,
    ):
        obj = model(**record)  # type: ignore
        if exclude:
            obj.__state__.exclude = exclude
        return obj
