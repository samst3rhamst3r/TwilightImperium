from dataclasses import dataclass

from app.config.base import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFlavorText:
    flavor_text: str

@dataclass(slots=True, frozen=True, kw_only=True)
class PlanetTextConfig(ConfigObj, RequiresFlavorText):
    pass
