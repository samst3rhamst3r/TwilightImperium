from .location_type import UnitLocationType
from .unit_class import UnitClass

VALID_LOCATIONS_BY_CONFIG_ID: dict[str, tuple[UnitLocationType, ...]] = {
    "floating_factory_i":   (UnitLocationType.SYSTEM,                                                       ),
    "floating_factory_ii":  (UnitLocationType.SYSTEM,                                                       )
}

VALID_LOCATIONS_BY_UNIT_CLASS: dict[UnitClass, tuple[UnitLocationType, ...]] = {
    UnitClass.CARRIER:      (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.CRUISER:      (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.DESTROYER:    (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.DREADNOUGHT:  (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.FLAGSHIP:     (UnitLocationType.SYSTEM,                                                       ),
    UnitClass.FIGHTER:      (UnitLocationType.SYSTEM,                               UnitLocationType.SHIP,  ),
    UnitClass.INFANTRY:     (                           UnitLocationType.PLANET,    UnitLocationType.SHIP,  ),
    UnitClass.PDS:          (                           UnitLocationType.PLANET,                            ),
    UnitClass.SPACE_DOCK:   (                           UnitLocationType.PLANET,                            ),
    UnitClass.WAR_SUN:      (UnitLocationType.SYSTEM,                                                       )
}