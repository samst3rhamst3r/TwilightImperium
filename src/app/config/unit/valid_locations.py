from .location_type import UnitLocationType
from .unit_class import UnitClass
from .ids import UnitID
from .unit import UnitConfig

VALID_LOCATIONS_BY_CONFIG_ID: dict[str, tuple[UnitLocationType, ...]] = {
    UnitID.FLOATING_FACTORY_I:  (UnitLocationType.SYSTEM,                                                       ),
    UnitID.FLOATING_FACTORY_II: (UnitLocationType.SYSTEM,                                                       )
}

VALID_LOCATIONS_BY_UNIT_CLASS: dict[UnitClass, tuple[UnitLocationType, ...]] = {
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
}

def get_valid_locations_for(unit: UnitConfig) -> tuple[UnitLocationType, ...]:
    if unit.id in VALID_LOCATIONS_BY_CONFIG_ID:
        return VALID_LOCATIONS_BY_CONFIG_ID[unit.id]
    return VALID_LOCATIONS_BY_UNIT_CLASS[unit.unit_class]