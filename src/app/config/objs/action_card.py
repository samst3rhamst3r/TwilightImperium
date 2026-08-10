from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import RequiresFlavorTextOptions, RequiresFunctionalText

@dataclass(frozen=True, kw_only=True)
class ActionCardConfig(NamedConfigObj, RequiresFunctionalText, RequiresFlavorTextOptions):
    num_in_deck: int = 1