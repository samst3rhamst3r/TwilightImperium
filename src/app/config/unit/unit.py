from dataclasses import dataclass, field
from collections.abc import Sequence
from typing import Optional

from app.config.ability import ParameterizedAbilityInstanceConfig
from app.config.shared import BaseConfigObj, FactionExclusiveConfigObj
from app.config.tech import TechUpgradeReqConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitLevelConfig(BaseConfigObj):
    cost: int = 0
    units_per_cost: int = 1
    combat: int = 0
    burst: int = 1
    move: int = 0
    capacity: int = 0
    ability_ids: Optional[Sequence[str]] = field(default_factory=tuple)
    parameterized_abilities: Optional[Sequence[ParameterizedAbilityInstanceConfig]] = field(default_factory=tuple)

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitConfig(FactionExclusiveConfigObj):
    level_1: Optional[UnitLevelConfig] = None
    upgrade_reqs: Optional[Sequence[TechUpgradeReqConfig]] = field(default_factory=tuple)
    level_2: Optional[UnitLevelConfig] = None

    def __post_init__(self):
        if self.level_1 is None and (len(self.upgrade_reqs) == 0 or self.level_2 is None):
            raise ValueError("If Level 1 is not provided, at least one upgrade requirement must be provided, and Level 2 must be provided.")
        if self.level_1 is not None and len(self.upgrade_reqs) > 0 and self.level_2 is None:
            raise ValueError("If Level 1 is provided and at least one upgrade requirement is provided, Level 2 must also be provided.")
        if self.level_1 is not None and len(self.upgrade_reqs) == 0 and self.level_2 is not None:
            raise ValueError("If Level 1 is provided and no upgrade requirements are provided, Level 2 must not be provided.")
