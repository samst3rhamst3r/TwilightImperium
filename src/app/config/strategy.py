from dataclasses import dataclass

from .shared.obj_ import NamedConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class StrategyConfig(NamedConfigObj):
    initiative: int