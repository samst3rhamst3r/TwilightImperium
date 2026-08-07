from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import PrimarySecondaryAbilityTextConfig

@dataclass(slots=True, frozen=True, kw_only=True)
class StrategyCardConfig(NamedConfigObj, PrimarySecondaryAbilityTextConfig):
    initiative: int