from dataclasses import dataclass

from app.config.shared import NamedConfigObj, RequiresFunctionalText, CanHaveFactionExclusivity

@dataclass(frozen=True, kw_only=True)
class AbilityConfig(NamedConfigObj, CanHaveFactionExclusivity, RequiresFunctionalText):
    # TODO: Add trigger fields for ability objects as they are defined
    # trigger: AbilityTrigger
    # trigger_event: GameEvent | None = None
    ...
