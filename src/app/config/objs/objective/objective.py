from dataclasses import dataclass
from types import MappingProxyType

from app.config.shared import NamedConfigObj
from app.config.shared.mixins import RequiresFunctionalText
from app.config.game_phase import GamePhase

from .type import ObjectiveType

_OBJECTIVE_POINTS_BY_TYPE: MappingProxyType[ObjectiveType, int] = MappingProxyType({
    ObjectiveType.PUBLIC_STAGE_I: 1,
    ObjectiveType.PUBLIC_STAGE_II: 2,
    ObjectiveType.SECRET: 1
})

@dataclass(slots=True, frozen=True, kw_only=True)
class ObjectiveConfig(NamedConfigObj, RequiresFunctionalText):
    objective_type: ObjectiveType
    phase: GamePhase

    @property
    def victory_points(self) -> int:
        return _OBJECTIVE_POINTS_BY_TYPE[self.objective_type]
