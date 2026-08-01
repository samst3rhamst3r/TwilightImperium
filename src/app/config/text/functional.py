from dataclasses import dataclass

from .base import BaseTextConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class RequiresFunctionalText:
    functional_text: str

@dataclass(slots=True, frozen=True, kw_only=True)
class FunctionalTextConfig(BaseTextConfigObj, RequiresFunctionalText):
    pass
