from dataclasses import dataclass

from app.config.tech import TechConfig
from app.config.text import FunctionalTextConfig

from .base import ConfigBasedStateObj
from .shared import PlayerOwnable

@dataclass(slots=True, kw_only=True)
class TechnologyCardState(ConfigBasedStateObj[TechConfig, FunctionalTextConfig], PlayerOwnable):
    pass
    