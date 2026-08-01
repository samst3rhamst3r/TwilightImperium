from dataclasses import dataclass
from typing import Optional

from app.config.planet import PlanetConfig

from .base import BaseStateObj
from .shared.exhaustable import Exhaustable

@dataclass(slots=True, kw_only=True)
class PlanetState(BaseStateObj[PlanetConfig], Exhaustable):
    is_controlled_by: Optional[str] = None