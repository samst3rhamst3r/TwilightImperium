from dataclasses import dataclass

from .named import NamedConfigObj
from .mixins import RequiresFlavorTextOptions, RequiresFunctionalText

@dataclass(frozen=True, kw_only=True)
class ActionCardConfig(NamedConfigObj, RequiresFunctionalText, RequiresFlavorTextOptions):
    num_in_deck: int = 1
    