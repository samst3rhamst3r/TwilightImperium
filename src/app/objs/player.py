
from typing import Iterable
import dataclasses as dc

from .named import NamedObject

type Planet = Planet

@dc.dataclass(slots=True)
class Player(NamedObject):
    name: str = dc.InitVar[str]
    planets: Iterable[Planet] = dc.field(default_factory=set)

    def __post_init__(self, name: str) -> None:
        NamedObject.__init__(self, name)

    def gain_planets(self, planets: Iterable[Planet]) -> None:
        self.planets.update(planets)

    def has_planets(self, planets: Iterable[Planet]) -> bool:
        return self.planets.issuperset(planets)
    
    def has_planet(self, planet: Planet) -> bool:
        return planet in self.planets