from dataclasses import dataclass, field
from typing import Optional
from collections.abc import Sequence

from .shared.obj_ import ConfigObj, ConfigRefObj, BaseConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class UniqueUnitsRefConfig(BaseConfigObj):
    carrier: Optional[ConfigRefObj] = None
    cruiser: Optional[ConfigRefObj] = None
    destroyer: Optional[ConfigRefObj] = None
    dreadnought: Optional[ConfigRefObj] = None
    fighter: Optional[ConfigRefObj] = None
    infantry: Optional[ConfigRefObj] = None
    pds: Optional[ConfigRefObj] = None
    space_dock: Optional[ConfigRefObj] = None
    war_sun: Optional[ConfigRefObj] = None

@dataclass(slots=True, frozen=True, kw_only=True)
class StartingUnitsConfig(BaseConfigObj):
    flagship: int = 0
    carrier: int = 0
    cruiser: int = 0
    dreadnought: int = 0
    destroyer: int = 0
    fighter: int = 0
    infantry: int = 0
    space_dock: int = 0
    pds: int = 0
    war_sun: int = 0

@dataclass(slots=True, frozen=True, kw_only=True)
class FactionConfig(ConfigObj):
    name: str
    home_systems: Sequence[ConfigRefObj]
    max_commodities: int
    abilities: Sequence[ConfigRefObj]
    flagship: ConfigRefObj
    starting_units: StartingUnitsConfig

    start_techs: Optional[Sequence[ConfigRefObj]] = field(default_factory=tuple)
    unique_techs: Optional[Sequence[ConfigRefObj]] = field(default_factory=tuple)
    unique_units: Optional[UniqueUnitsRefConfig] = field(default_factory=UniqueUnitsRefConfig)
