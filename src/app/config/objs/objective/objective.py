from dataclasses import dataclass
from types import MappingProxyType

from app.config.fromdict import FromDictMixin
from app.config.objs.named import NamedConfigObj
from app.config.objs.mixins import RequiresFunctionalText
from app.config.game_phase import GamePhase

from .type import ObjectiveType

_OBJECTIVE_POINTS_BY_TYPE: MappingProxyType[ObjectiveType, int] = MappingProxyType({
    ObjectiveType.PUBLIC_STAGE_I: 1,
    ObjectiveType.PUBLIC_STAGE_II: 2,
    ObjectiveType.SECRET: 1
})

@dataclass(frozen=True, kw_only=True)
class ObjectiveConfig(NamedConfigObj, RequiresFunctionalText, FromDictMixin):
    objective_type: ObjectiveType
    game_phase: GamePhase

    @property
    def victory_points(self) -> int:
        return _OBJECTIVE_POINTS_BY_TYPE[self.objective_type]

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["objective_type"] = ObjectiveType(d["objective_type"])
        d["game_phase"] = GamePhase(d["game_phase"])