from dataclasses import dataclass, field
from collections.abc import Sequence
from typing import Optional

from app.config.ability import ParameterizedAbilityInstanceConfig
from app.config.shared import FactionExclusiveConfigObj
from app.config.tech import TechUpgradeReqConfig

from .unit_class import UnitClass

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitConfig(FactionExclusiveConfigObj):

    unit_class: UnitClass

    cost: int | None
    combat: int | None
    move: int | None
    capacity: int | None
    units_per_cost: int | None = 1
    burst: int | None = 1

    ability_ids: Sequence[str] = field(default_factory=tuple)
    parameterized_abilities: Sequence[ParameterizedAbilityInstanceConfig] = field(default_factory=tuple)
    upgraded_from: Optional[str] = None
    upgrade_reqs: Sequence[TechUpgradeReqConfig] = field(default_factory=tuple)
