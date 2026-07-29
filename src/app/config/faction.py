from dataclasses import dataclass, field
from typing import Optional
from collections.abc import Sequence

from .shared.obj_ import ConfigObj, ConfigRefObj, BaseConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class UniqueUnitsRefConfig(BaseConfigObj):
    flagship: ConfigRefObj
    carrier: ConfigRefObj = None
    cruiser: ConfigRefObj = None
    dreadnought: ConfigRefObj = None
    destroyer: ConfigRefObj = None
    fighter: ConfigRefObj = None
    infantry: ConfigRefObj = None
    space_dock: ConfigRefObj = None
    pds: ConfigRefObj = None
    war_sun: ConfigRefObj = None

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
    max_commodities: int
    home_systems: Sequence[ConfigRefObj]
    abilities: Sequence[ConfigRefObj]
    unique_units: UniqueUnitsRefConfig
    starting_units: StartingUnitsConfig

    start_techs: Optional[Sequence[ConfigRefObj]] = field(default_factory=tuple)
    unique_techs: Optional[Sequence[ConfigRefObj]] = field(default_factory=tuple)
