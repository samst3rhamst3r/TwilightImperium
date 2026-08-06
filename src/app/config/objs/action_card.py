from dataclasses import dataclass

from ..shared import NamedConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class ActionCardConfig(NamedConfigObj):
    pass