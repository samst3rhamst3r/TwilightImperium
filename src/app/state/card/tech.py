from dataclasses import dataclass

from app.config.tech import TechConfig
from app.config.text import FunctionalTextConfig

from app.state.base.state_obj import ConfigBoundStateObj, TextBoundStateObjMixin

@dataclass(slots=True, kw_only=True)
class TechnologyCardState(ConfigBoundStateObj[TechConfig], TextBoundStateObjMixin[FunctionalTextConfig]):
    pass
    