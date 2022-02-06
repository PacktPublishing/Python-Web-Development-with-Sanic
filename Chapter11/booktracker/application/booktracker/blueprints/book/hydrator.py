from json import loads
from typing import Any, List, Mapping, Optional, Type, TypeVar

from booktracker.blueprints.author.model import Author
from booktracker.blueprints.book.model import Series
from booktracker.common.base_model import BaseModel
from booktracker.common.dao.hydrator import Hydrator

T = TypeVar("T", bound=BaseModel)


class BookHydrator(Hydrator):
    def do_hydration(
        self,
        record: Mapping[str, Any],
        model: Type[T],
        exclude: Optional[List[str]] = None,
    ) -> T:
        series = Series(**loads(record["series"])) if record["series"] else None
        kwargs = {
            **record,
            "author": Author(**loads(record["author"])),
            "series": series,
        }
        obj = model(**kwargs)
        if exclude:
            obj.set_state("exclude", exclude)

        return obj
