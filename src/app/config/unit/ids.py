import enum

class UnitID(enum.StrEnum):
    """Unit IDs can be enumerated here if there are unit-specific 
    configurations required that don't belong in YAML config files
    """
    FLOATING_FACTORY_I = enum.auto()
    FLOATING_FACTORY_II = enum.auto()
