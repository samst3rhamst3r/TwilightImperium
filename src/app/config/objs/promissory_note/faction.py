from dataclasses import dataclass

from app.config.objs.mixins import RequiresFunctionalText, RequiresFactionExclusivity
from .base import PromissoryNoteConfig

@dataclass(frozen=True, kw_only=True)
class FactionPromissoryNoteConfig(PromissoryNoteConfig, RequiresFactionExclusivity, RequiresFunctionalText):
    pass
