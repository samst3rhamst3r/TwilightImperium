from dataclasses import dataclass

from app.config.shared.text_objs import RequiresFlavorTextOptions, RequiresFunctionalText

from ..shared import NamedConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class ActionCardConfig(NamedConfigObj, RequiresFunctionalText, RequiresFlavorTextOptions):
    pass