from dataclasses import dataclass

from app.state.objs.unit import UnitState
from app.config.objs.unit import UnitConfig

from .base import BaseResolvedObj

@dataclass(slots=True, frozen=True)
class ResolvedUnit(BaseResolvedObj[UnitState, UnitConfig]):
    pass