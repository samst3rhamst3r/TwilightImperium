from dataclasses import dataclass

from app.config.objective import ObjectiveConfig
from app.config.text import FunctionalTextConfig
from app.state.base import ConfigIDBasedStateObj

@dataclass(slots=True, kw_only=True)
class ObjectiveCardState(ConfigIDBasedStateObj[ObjectiveConfig, FunctionalTextConfig]):

    @property
    def victory_points(self) -> int:
        return self.config.victory_points