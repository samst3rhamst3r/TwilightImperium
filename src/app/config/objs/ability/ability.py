from dataclasses import dataclass

from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import RequiresFunctionalText, CanHaveFactionExclusivity

@dataclass(frozen=True, kw_only=True)
class AbilityConfig(NamedConfigObj, CanHaveFactionExclusivity, RequiresFunctionalText):
    # TODO: Add trigger fields for ability objects as they are defined
    # trigger: AbilityTrigger
    # trigger_event: GameEvent | None = None
    ...
