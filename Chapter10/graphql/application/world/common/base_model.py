from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import List, TypeVar, Union
from uuid import UUID

import ujson

T = TypeVar("T")


@dataclass
class MetaState:
    exclude: List[str] = field(default_factory=list)


class BaseModel:
    __state__: MetaState

    def __post_init__(self) -> None:
        self.__state__ = MetaState()

    def __json__(self) -> str:
        return ujson.dumps(
            {
                k: self._clean(v)
                for k, v in asdict(self).items()
                if k not in self.__state__.exclude
            }
        )

    @staticmethod
    def _clean(value: T) -> Union[str, T]:
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, UUID):
            return str(value)
        return value
