from dataclasses import dataclass

from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import RequiresFunctionalText, RequiresFactionExclusivity

@dataclass(frozen=True, kw_only=True)
class FactionPromissoryNoteConfig(NamedConfigObj, RequiresFactionExclusivity, RequiresFunctionalText):
    pass
