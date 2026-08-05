from dataclasses import dataclass
from typing import Self

from app.config.tech import TechConfig
from app.config.text import FunctionalTextConfig

from app.state.base.state_obj import ConfigBoundStateObj, TextBoundStateObjMixin

@dataclass(slots=True, kw_only=True)
class TechnologyCardState(ConfigBoundStateObj[TechConfig], TextBoundStateObjMixin[FunctionalTextConfig]):

    def to_save_dict(self):
        d = ConfigBoundStateObj.to_save_dict(self)
        d |= TextBoundStateObjMixin.to_save_dict(self)
        return d

    @classmethod
    def from_save_dict(cls, config: TechConfig, text_config: FunctionalTextConfig, **kwargs) -> Self:
        return cls(config=config, text_config=text_config, **kwargs)
    