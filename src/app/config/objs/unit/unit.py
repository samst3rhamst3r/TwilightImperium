from dataclasses import dataclass
from types import MappingProxyType

from app.config.fromdict import FromDictMixin
from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import CanHaveFactionExclusivity

from app.config.objs.ability import ParameterizedAbilityInstanceConfig, load_ability_config, load_parameterized_ability_instance
from app.config.objs.tech import TechUpgradeReqConfig

from .unit_class import UnitClass
from .location_type import UnitLocationType
from .unit_class import UnitClass
from .ids import UnitID

_VALID_LOCATIONS_BY_CONFIG_ID: MappingProxyType[str, tuple[UnitLocationType, ...]] = MappingProxyType({
    UnitID.FLOATING_FACTORY_I:  (UnitLocationType.SYSTEM,                                                       ),
    UnitID.FLOATING_FACTORY_II: (UnitLocationType.SYSTEM,                                                       )
})

_VALID_LOCATIONS_BY_UNIT_CLASS: MappingProxyType[UnitClass, tuple[UnitLocationType, ...]] = MappingProxyType({
    UnitClass.CARRIER:          (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.CRUISER:          (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.DESTROYER:        (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.DREADNOUGHT:      (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.FLAGSHIP:         (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.FIGHTER:          (UnitLocationType.SYSTEM,                               UnitLocationType.SHIP,  ),
    UnitClass.INFANTRY:         (                           UnitLocationType.PLANET,    UnitLocationType.SHIP,  ),
    UnitClass.PDS:              (                           UnitLocationType.PLANET,                            ),
    UnitClass.SPACE_DOCK:       (                           UnitLocationType.PLANET,                            ),
    UnitClass.WAR_SUN:          (UnitLocationType.SYSTEM,                                                       )
})

@dataclass(frozen=True, kw_only=True)
class UnitConfig(NamedConfigObj, CanHaveFactionExclusivity, FromDictMixin):
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

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["unit_class"] = UnitClass(d["unit_class"])
        d["ability_ids"] = tuple(d["ability_ids"])
        d["parameterized_abilities"] = tuple(load_parameterized_ability_instance(ability) for ability in d["parameterized_abilities"])
        d["upgrade_reqs"] = tuple(TechUpgradeReqConfig.from_dict(req) for req in d["upgrade_reqs"])

    @property
    def can_move(self) -> bool:
        return self.move is not None and self.move > 0

    @property
    def can_carry_units(self) -> bool:
        return self.capacity is not None and self.capacity > 0

    @property
    def valid_locations(self) -> tuple[UnitLocationType, ...]:
        if self.id in _VALID_LOCATIONS_BY_CONFIG_ID:
            return _VALID_LOCATIONS_BY_CONFIG_ID[self.id]
        return _VALID_LOCATIONS_BY_UNIT_CLASS[self.unit_class]

    @property
    def can_move_to_systems(self) -> bool:
        return UnitLocationType.SYSTEM in self.valid_locations