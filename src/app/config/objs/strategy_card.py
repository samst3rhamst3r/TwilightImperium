from dataclasses import dataclass

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import IsExhaustable

@dataclass(slots=True, frozen=True, kw_only=True)
class StrategyCardConfig(NamedConfigObj, IsExhaustable):
    initiative: int
    primary_ability_text: str
    secondary_ability_text: str
