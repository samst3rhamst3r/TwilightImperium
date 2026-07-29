from dataclasses import dataclass
from typing import Optional
import enum

from .tech import TechType
from .shared.obj_ import ConfigObj

class PlanetTrait(enum.StrEnum):
    CULTURAL = enum.auto()
    HAZARDOUS = enum.auto()
    INDUSTRIAL = enum.auto()

@dataclass(frozen=True, kw_only=True, slots=True)
class Planet(ConfigObj):
    name: str
    resources: int = 0
    influence: int = 0
    tech_specialty: Optional[TechType] = None
    trait: Optional[PlanetTrait] = None
