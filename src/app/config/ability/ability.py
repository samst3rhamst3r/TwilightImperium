from dataclasses import dataclass

from app.config.base import CanHaveFactionExclusivity

@dataclass(slots=True, frozen=True, kw_only=True)
class AbilityConfig(CanHaveFactionExclusivity):
    pass
