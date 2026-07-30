from dataclasses import dataclass, field
from collections.abc import Sequence

from .shared.obj_ import BaseConfigObj, ConfigObj
from .tech_req import TechReqConfig
from .ability import AbilityRefConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitLevelConfig(BaseConfigObj):
    cost: int = 0
    units_per_cost: int = 1
    combat: int = 0
    burst: int = 1
    move: int = 0
    capacity: int = 0
    abilities: Sequence[AbilityRefConfig] = field(default_factory=tuple)

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitConfig(ConfigObj):
    name: str
    level_1: UnitLevelConfig
    upgrade_reqs: Sequence[TechReqConfig]
    level_2: UnitLevelConfig