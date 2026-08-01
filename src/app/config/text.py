from collections.abc import Sequence
from dataclasses import dataclass

from .base import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFunctionalText:
    functional_text: str

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFlavorText:
    flavor_text: str

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFlavorTextOptions:
    flavor_text_options: Sequence[str]

@dataclass(slots=True, frozen=True, kw_only=True)
class FunctionalTextConfig(ConfigObj, RequiresFunctionalText):
    pass

@dataclass(slots=True, frozen=True, kw_only=True)
class FlavorTextConfig(ConfigObj, RequiresFlavorText):
    pass

@dataclass(slots=True, frozen=True, kw_only=True)
class FunctionalTextWithFlavorTextOptionsConfig(ConfigObj, RequiresFunctionalText, RequiresFlavorTextOptions):
    pass
