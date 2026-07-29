from dataclasses import dataclass, field
from collections.abc import Sequence

from .shared.obj_ import BaseConfigObj, ConfigObj
from .tech_req import TechReqConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitLevelConfig(BaseConfigObj):
    cost: int = 0
    combat: int = 0
    move: int = 0
    capacity: int = 0
    abilities: Sequence[str] = field(default_factory=tuple)

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitConfig(ConfigObj):
    name: str
    level_1_config: UnitLevelConfig
    upgrade_reqs: Sequence[TechReqConfig]
    level_2_config: UnitLevelConfig