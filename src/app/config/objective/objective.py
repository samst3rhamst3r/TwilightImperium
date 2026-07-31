from dataclasses import dataclass, field

from app.config.shared import NamedConfigObj
from app.config.game_phase import GamePhase

from .type import ObjectiveType

@dataclass(slots=True, frozen=True, kw_only=True)
class ObjectiveConfig(NamedConfigObj):
    type_: ObjectiveType = field(metadata={"key": "type"})
    victory_points: int
    phase: GamePhase
