from collections.abc import Sequence
from dataclasses import dataclass

from app.config.base import ConfigObj
from .text import RequiresFunctionalText

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFlavorTextOptions:
    flavor_text_options: Sequence[str]

@dataclass(slots=True, frozen=True, kw_only=True)
class EventTextConfig(ConfigObj, RequiresFunctionalText, RequiresFlavorTextOptions):
    pass
