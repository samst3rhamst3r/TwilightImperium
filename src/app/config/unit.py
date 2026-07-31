from dataclasses import dataclass, field
from collections.abc import Sequence

from .parameterized_abilities import ParameterizedAbilityConfig
from .shared.obj_ import BaseConfigObj, FactionExclusiveConfigObj
from .tech_req import TechReqConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitLevelConfig(BaseConfigObj):
    cost: int = 0
    units_per_cost: int = 1
    combat: int = 0
    burst: int = 1
    move: int = 0
    capacity: int = 0
    ability_ids: Sequence[str] = field(default_factory=tuple)
    parameterized_abilities: Sequence[ParameterizedAbilityConfig] = field(default_factory=tuple)

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitConfig(FactionExclusiveConfigObj):
    level_1: UnitLevelConfig
    upgrade_reqs: Sequence[TechReqConfig]
    level_2: UnitLevelConfig