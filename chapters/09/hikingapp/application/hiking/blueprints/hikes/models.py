from dataclasses import dataclass
from hiking.common.base_model import BaseModel
from datetime import date

from hiking.blueprints.trails.models import Trail


@dataclass
class Hike(BaseModel):
    trail: Trail
    date: date
