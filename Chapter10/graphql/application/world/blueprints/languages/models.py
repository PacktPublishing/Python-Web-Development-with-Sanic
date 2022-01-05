from dataclasses import dataclass
from world.common.base_model import BaseModel


@dataclass
class Language(BaseModel):
    countrycode: str
    language: str
    isofficial: bool
    percentage: float
