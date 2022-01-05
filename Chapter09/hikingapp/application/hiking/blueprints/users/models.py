from dataclasses import dataclass, field
from hiking.common.base_model import BaseModel


@dataclass
class User(BaseModel):
    user_id: int
    name: str
    total_distance_hiked: float = field(default=0)
