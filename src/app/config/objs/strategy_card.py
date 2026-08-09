from dataclasses import dataclass

from app.config.shared import NamedConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class StrategyCardConfig(NamedConfigObj):
    initiative: int
    primary_ability_text: str
    secondary_ability_text: str
