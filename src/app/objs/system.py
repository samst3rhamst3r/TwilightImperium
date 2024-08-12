import dataclasses as dc
import enum
from typing import Iterable

from .planet import Planet

class Wormhole(enum.Enum):
    ALPHA = enum.auto()
    BETA = enum.auto()
    DELTA = enum.auto()

class Anomaly(enum.Enum):
    ASTEROID_FIELD = enum.auto()
    NEBULA = enum.auto()
    SUPERNOVA = enum.auto()
    GRAVITY_RIFT = enum.auto()

@dc.dataclass(slots=True)
class System:
    planets: tuple[Planet] | None = None
    wormholes: tuple[Wormhole] | None = None
    anomaly: Anomaly | None = None
    neighbors: tuple = dc.field(init=False)

    def has_planet(self, planet: str | Planet):
        if isinstance(planet, str):
            return planet in (planet_.name for planet_ in self.planets)
        else:
            return planet in self.planets
        
    def has_wormhole(self, wormhole: str | Wormhole):
        if isinstance(wormhole, str):
            return wormhole in (wormhole_.name for wormhole_ in self.wormholes)
        else:
            return wormhole in self.wormholes