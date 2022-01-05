from dataclasses import dataclass
from hiking.common.base_model import BaseModel
from decimal import Decimal


@dataclass
class Trail(BaseModel):
    trail_id: int
    name: str
    distance: Decimal
