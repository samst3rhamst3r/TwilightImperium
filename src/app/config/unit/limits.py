from types import MappingProxyType

from .unit_class import UnitClass

_UNIT_LIMITATIONS_BY_CLASS: MappingProxyType[UnitClass, int | None] = MappingProxyType({
    UnitClass.CARRIER: 4,
    UnitClass.CRUISER: 8,
    UnitClass.DESTROYER: 8,
    UnitClass.DREADNOUGHT: 5,
    UnitClass.FIGHTER: None,
    UnitClass.FLAGSHIP: 1,
    UnitClass.INFANTRY: None,
    UnitClass.PDS: 6,
    UnitClass.SPACE_DOCK: 3,
    UnitClass.WAR_SUN: 2,
})

_COMPONENT_LIMITATIONS_BY_CLASS: MappingProxyType[str, int] = MappingProxyType({
    UnitClass.FIGHTER: 10,
    UnitClass.INFANTRY: 12,
})

def get_unit_limit(unit_class: UnitClass) -> int | None:
    return _UNIT_LIMITATIONS_BY_CLASS[unit_class]

def get_component_limit(unit_class: UnitClass) -> int:
    return _COMPONENT_LIMITATIONS_BY_CLASS.get(unit_class, _UNIT_LIMITATIONS_BY_CLASS[unit_class])
