import enum

class UnitClass(enum.StrEnum):
    CARRIER = enum.auto()
    CRUISER = enum.auto()
    DESTROYER = enum.auto()
    DREADNOUGHT = enum.auto()
    FLAGSHIP = enum.auto()
    FIGHTER = enum.auto()
    INFANTRY = enum.auto()
    PDS = enum.auto()
    SPACE_DOCK = enum.auto()
    WAR_SUN = enum.auto()
