from enum import auto

from app.config.shared.enum import ConfigEnum

class UnitID(ConfigEnum):
    """Unit IDs can be enumerated here if there are unit-specific 
    configurations required that don't belong in YAML config files
    """
    FLOATING_FACTORY_I = auto()
    FLOATING_FACTORY_II = auto()
