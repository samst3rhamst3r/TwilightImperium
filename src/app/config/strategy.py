from dataclasses import dataclass

from .shared.obj_ import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class StrategyCardConfig(ConfigObj):
    name: str
    initiative: int