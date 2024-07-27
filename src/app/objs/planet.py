import dataclasses as dc
import enum

from app.objs.tech import TechType

class PlanetTrait(enum.Enum):
    CULTURAL = enum.auto()
    HAZARDOUS = enum.auto()
    INDUSTRIAL = enum.auto()

@dc.dataclass(slots=True)
class Planet:
    name: str
    resources: int = 0
    influence: int = 0
    tech_specialty: TechType | None = None
    trait: PlanetTrait | None = None
    exhausted: bool = False