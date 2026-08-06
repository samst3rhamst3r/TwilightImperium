from dataclasses import dataclass

from .base import NamedConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class ActionCardConfig(NamedConfigObj):
    pass