from types import MappingProxyType

from .location_type import UnitLocationType
from .unit_class import UnitClass
from .ids import UnitID
from .unit import UnitConfig

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

def get_valid_locations_for(unit: UnitConfig) -> tuple[UnitLocationType, ...]:
    if unit.id in _VALID_LOCATIONS_BY_CONFIG_ID:
        return _VALID_LOCATIONS_BY_CONFIG_ID[unit.id]
    return _VALID_LOCATIONS_BY_UNIT_CLASS[unit.unit_class]