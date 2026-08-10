from dataclasses import dataclass

from app.config.shared import NamedConfigObj, CanHaveFactionExclusivity

from app.config.objs.ability import ParameterizedAbilityInstanceConfig
from app.config.objs.tech import TechUpgradeReqConfig

from .unit_class import UnitClass

@dataclass(slots=True, frozen=True, kw_only=True)
class UnitConfig(NamedConfigObj, CanHaveFactionExclusivity):
    """Unlike most Config types, functional_text is optional here (not the
    mandatory RequiresFunctionalText mixin) - plenty of units (e.g. basic
    Cruisers, Destroyers) have no special ability text at all."""

    unit_class: UnitClass

    cost: int | None
    combat: int | None
    move: int | None
    capacity: int | None
    units_per_cost: int | None = 1
    burst: int | None = 1

    functional_text: str | None = None

    ability_ids: tuple[str, ...] = ()
    parameterized_abilities: tuple[ParameterizedAbilityInstanceConfig, ...] = ()
    upgraded_from_unit_id: str | None = None
    upgrade_reqs: tuple[TechUpgradeReqConfig, ...] = ()

    def __post_init__(self):
        object.__setattr__(self, "unit_class", UnitClass(self.unit_class))

    @property
    def can_move(self) -> bool:
        return self.move is not None and self.move > 0

    @property
    def can_carry_units(self) -> bool:
        return self.capacity is not None and self.capacity > 0