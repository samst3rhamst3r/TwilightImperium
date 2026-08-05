from dataclasses import dataclass

from app.config.objective import ObjectiveConfig
from app.config.text import FunctionalTextConfig
from app.state.base.state_obj import ConfigIDBasedStateObj, TextBoundStateObjMixin

@dataclass(slots=True, kw_only=True)
class ObjectiveCardState(ConfigIDBasedStateObj[ObjectiveConfig], TextBoundStateObjMixin[FunctionalTextConfig]):

    def to_save_dict(self):
        d = ConfigIDBasedStateObj[ObjectiveConfig].to_save_dict(self)
        return d | TextBoundStateObjMixin[FunctionalTextConfig].to_save_dict(self)

    @staticmethod
    def init_from_save_dict(data: dict) -> dict[str, int]:
        d = ConfigIDBasedStateObj[ObjectiveConfig].init_from_save_dict(data)
        return d | TextBoundStateObjMixin[FunctionalTextConfig].init_from_save_dict(data)
    
    @property
    def victory_points(self) -> int:
        return self.config.victory_points