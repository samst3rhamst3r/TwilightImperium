from dataclasses import dataclass
from typing import Optional

from app.config.planet import PlanetConfig
from app.config.text import PlanetTextConfig

from .base import ConfigIDStateObj
from .shared.exhaustable import Exhaustable

@dataclass(slots=True, kw_only=True)
class PlanetState(ConfigIDStateObj[PlanetConfig, PlanetTextConfig], Exhaustable):
    is_controlled_by: Optional[str] = None