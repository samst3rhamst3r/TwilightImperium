from collections.abc import Sequence
from dataclasses import dataclass

from .base import BaseTextConfigObj
from .functional import RequiresFunctionalText

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFlavorTextOptions:
    flavor_text_options: Sequence[str]

@dataclass(slots=True, frozen=True, kw_only=True)
class EventTextConfig(BaseTextConfigObj, RequiresFunctionalText, RequiresFlavorTextOptions):
    pass
