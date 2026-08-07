from dataclasses import dataclass

from app.state.unit import UnitState
from app.config.objs.unit import UnitConfig

from .base import BaseResolvedObj
from .shared.protocols import CanHaveFactionExclusivityMixin, ResolvedFunctionalTextMixin

@dataclass(slots=True, frozen=True)
class ResolvedUnit(BaseResolvedObj[UnitState, UnitConfig], CanHaveFactionExclusivityMixin, ResolvedFunctionalTextMixin):
    pass