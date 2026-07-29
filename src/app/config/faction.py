from dataclasses import dataclass
from typing import Optional
from collections.abc import Sequence

from .shared.obj_ import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class FactionConfig(ConfigObj):
    name: str
    max_commodities: int    
    units: Optional[Sequence] = None
    techs: Optional[Sequence] = None
    home_systems: Optional[Sequence] = None
