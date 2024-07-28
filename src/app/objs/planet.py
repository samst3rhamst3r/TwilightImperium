import dataclasses as dc
import enum

from .named import NamedObject
from .tech import TechType
from .exhaustable import Exhaustable
from .player import Player

class PlanetTrait(enum.Enum):
    CULTURAL = enum.auto()
    HAZARDOUS = enum.auto()
    INDUSTRIAL = enum.auto()

@dc.dataclass(slots=True)
class Planet(NamedObject, Exhaustable):
    name: dc.InitVar[str]
    resources: int = 0
    influence: int = 0
    tech_specialty: TechType | str | None = None
    trait: PlanetTrait | str | None = None
    player: Player = None
    exhausted: dc.InitVar[bool] = False

    def __post_init__(self, name: str, exhausted: bool):
        NamedObject.__init__(self, name)
        Exhaustable.__init__(self, exhausted)

        if isinstance(self.trait, str):
            self.trait = PlanetTrait[self.trait.upper()]
        
        if isinstance(self.tech_specialty, str):
            self.tech_specialty = TechType[self.tech_specialty.upper()]
