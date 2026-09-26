from dataclasses import dataclass

from app.config.objs.mixins import RequiresFunctionalText, RequiresFactionExclusivity

from .base import AbilityConfig

@dataclass(frozen=True, kw_only=True)
class FactionAbilityConfig(AbilityConfig, RequiresFactionExclusivity, RequiresFunctionalText):
    pass
