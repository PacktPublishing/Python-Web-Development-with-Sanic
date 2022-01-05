from dataclasses import dataclass
from world.common.base_model import BaseModel


@dataclass
class Country(BaseModel):
    code: str
    name: str
    continent: str
    region: str
    surfacearea: int
    indepyear: int
    population: int
    lifeexpectancy: int
    gnp: float
    gnpold: float
    localname: str
    governmentform: str
    headofstate: str
    capital: int
    code2: str
