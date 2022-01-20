from json import loads
from typing import Any, List, Mapping, Optional, Type

from booktracker.blueprints.author.model import Author
from booktracker.blueprints.book.model import Series
from booktracker.common.base_model import BaseModel
from booktracker.common.dao.hydrator import Hydrator


class BookHydrator(Hydrator):
    def do_hydration(
        self,
        record: Mapping[str, Any],
        model: Type[BaseModel],
        exclude: Optional[List[str]] = None,
    ):
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
