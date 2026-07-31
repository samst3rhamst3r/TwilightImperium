from dataclasses import dataclass

from app.config.shared import FactionExclusiveConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class AbilityConfig(FactionExclusiveConfigObj):
    pass
