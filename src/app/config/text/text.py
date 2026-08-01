from dataclasses import dataclass

from app.config.base import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFunctionalText:
    functional_text: str

@dataclass(slots=True, frozen=True, kw_only=True)
class FunctionalTextConfig(ConfigObj, RequiresFunctionalText):
    pass
