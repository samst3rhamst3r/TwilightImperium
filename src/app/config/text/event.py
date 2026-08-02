from dataclasses import dataclass

from .base import BaseTextConfigObj
from .functional import RequiresFunctionalText

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFlavorTextOptions:
    flavor_text_options: tuple[str, ...]

@dataclass(slots=True, frozen=True, kw_only=True)
class EventTextConfig(BaseTextConfigObj, RequiresFunctionalText, RequiresFlavorTextOptions):
    pass
