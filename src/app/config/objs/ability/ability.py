from dataclasses import dataclass

from app.config.shared.text_objs import RequiresFunctionalText
from app.config.shared import CanHaveFactionExclusivity

@dataclass(slots=True, frozen=True, kw_only=True)
class AbilityConfig(CanHaveFactionExclusivity, RequiresFunctionalText):
    # TODO: Add trigger fields for ability objects as they are defined
    # trigger: AbilityTrigger
    # trigger_event: GameEvent | None = None
    ...
