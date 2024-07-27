import dataclasses as dc
import enum

from .tech import TechType
from .exhaustable import Exhaustable

class PlanetTrait(enum.Enum):
    CULTURAL = enum.auto()
    HAZARDOUS = enum.auto()
    INDUSTRIAL = enum.auto()

@dc.dataclass(slots=True)
class Planet(Exhaustable):
    name: str
    resources: int = 0
    influence: int = 0
    tech_specialty: TechType | None = None
    trait: PlanetTrait | str | None = None

    player = None
    exhausted: dc.InitVar[bool] = False

    def __post_init__(self, exhausted: bool):
        super().__init__(exhausted)
        if isinstance(self.trait, str):
            self.trait = PlanetTrait[self.trait.upper()]