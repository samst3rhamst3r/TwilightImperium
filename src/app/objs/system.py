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
    wormhole: tuple[Wormhole] | None = None
    anomaly: Anomaly | None = None
    neighbors: tuple = dc.field(init=False)
