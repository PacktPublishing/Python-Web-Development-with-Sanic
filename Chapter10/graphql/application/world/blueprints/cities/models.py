from dataclasses import dataclass

from world.common.base_model import BaseModel


@dataclass
class City(BaseModel):
    id: int
    name: str
    countrycode: str
    district: str
    population: int
