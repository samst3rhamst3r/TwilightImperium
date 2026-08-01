from dataclasses import dataclass

from .base import BaseTextConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFlavorText:
    flavor_text: str

@dataclass(slots=True, frozen=True, kw_only=True)
class PlanetTextConfig(BaseTextConfigObj, RequiresFlavorText):
    pass
