from dataclasses import dataclass

from .base import BaseTextConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class StrategyTextConfig(BaseTextConfigObj):
    primary_ability_text: str
    secondary_ability_text: str
    