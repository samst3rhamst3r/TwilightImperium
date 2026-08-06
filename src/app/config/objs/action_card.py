from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.text_objs import RequiresFlavorTextOptions, RequiresFunctionalText

@dataclass(slots=True, frozen=True, kw_only=True)
class ActionCardConfig(NamedConfigObj, RequiresFunctionalText, RequiresFlavorTextOptions):
    pass