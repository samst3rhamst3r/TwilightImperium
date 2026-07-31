from dataclasses import dataclass

from .shared.obj_ import FactionExclusiveConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class AbilityConfig(FactionExclusiveConfigObj):
    pass
