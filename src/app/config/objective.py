from dataclasses import dataclass, field
from typing import Union

from .shared.obj_ import ConfigObj
from ..types.objective import ObjectiveType
from ..types.game_phase import GamePhase

@dataclass(slots=True, frozen=True, kw_only=True)
class ObjectiveCardConfig(ConfigObj):
    name: str
    type_: ObjectiveType = field(metadata={"key": "type"})
    victory_points: int
    phase: Union[GamePhase.STATUS, GamePhase.ACTION] = GamePhase.STATUS
    num_in_deck: int = 1