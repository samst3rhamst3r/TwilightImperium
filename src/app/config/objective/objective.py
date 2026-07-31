from dataclasses import dataclass, field

from app.config.shared import NamedConfigObj
from app.config.game.phase import GamePhase

from .type import ObjectiveType

OBJECTIVE_POINTS_BY_TYPE = {
    ObjectiveType.STAGE_I: 1,
    ObjectiveType.STAGE_II: 2,
    ObjectiveType.SECRET: 1
}

@dataclass(slots=True, frozen=True, kw_only=True)
class ObjectiveConfig(NamedConfigObj):
    type_: ObjectiveType = field(metadata={"key": "type"})
    phase: GamePhase

    @property
    def victory_points(self) -> int:
        return OBJECTIVE_POINTS_BY_TYPE[self.type_]
