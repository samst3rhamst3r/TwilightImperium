from dataclasses import dataclass

from app.config.base import CanHaveFactionExclusivity

@dataclass(slots=True, frozen=True, kw_only=True)
class AbilityConfig(CanHaveFactionExclusivity):
    # TODO: Add trigger fields for ability objects as they are defined
    # trigger: AbilityTrigger
    # trigger_event: GameEvent | None = None
    ...
