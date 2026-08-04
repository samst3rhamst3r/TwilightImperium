from dataclasses import dataclass

from app.config.tech import TechConfig
from app.config.text import FunctionalTextConfig

from .base import ConfigBoundStateObj, TextBoundStateObjMixin
from .shared import PlayerOwnable

@dataclass(slots=True, kw_only=True)
class TechnologyCardState(ConfigBoundStateObj[TechConfig], TextBoundStateObjMixin[FunctionalTextConfig], PlayerOwnable):
    pass
    