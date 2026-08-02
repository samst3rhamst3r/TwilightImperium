from dataclasses import dataclass

from app.config.ability import ParameterizedAbilityInstanceConfig
from app.config.base import CanHaveFactionExclusivity
from app.config.tech import TechUpgradeReqConfig

from .unit_class import UnitClass

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitConfig(CanHaveFactionExclusivity):

    unit_class: UnitClass

    cost: int | None
    combat: int | None
    move: int | None
    capacity: int | None
    units_per_cost: int | None = 1
    burst: int | None = 1

    ability_ids: tuple[str, ...] = ()
    parameterized_abilities: tuple[ParameterizedAbilityInstanceConfig, ...] = ()
    upgraded_from: str | None = None
    upgrade_reqs: tuple[TechUpgradeReqConfig, ...] = ()

    @property
    def can_move(self) -> bool:
        return self.move is not None and self.move > 0

    @property
    def can_carry_units(self) -> bool:
        return self.capacity is not None and self.capacity > 0