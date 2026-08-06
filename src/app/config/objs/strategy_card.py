from dataclasses import dataclass

from app.config.shared.text_objs import PrimarySecondaryAbilityTextConfig
from app.config.shared import NamedConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class StrategyCardConfig(NamedConfigObj, PrimarySecondaryAbilityTextConfig):
    initiative: int