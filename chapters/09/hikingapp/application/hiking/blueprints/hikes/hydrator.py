from typing import Any, List, Mapping, Optional, Type, Union
from hiking.common.dao.hydrator import Hydrator
from hiking.common.base_model import BaseModel
from hiking.blueprints.hikes.models import Hike
from hiking.blueprints.trails.models import Trail


class HikeHydrator(Hydrator):
    def do_hydration(
        self,
        record: Mapping[str, Any],
        model: Type[BaseModel],
        exclude: Optional[List[str]] = None,
    ):
        values = dict(record)
        date = values.pop("date")
        return Hike(Trail(**values), date)
