from dataclasses import dataclass

from app.config.base import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class StrategyTextConfig(ConfigObj):
    primary_ability_text: str
    secondary_ability_text: str
    