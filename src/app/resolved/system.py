from dataclasses import dataclass

from app.state.system import SystemState
from app.config.objs.system import SystemConfig

from .base import BaseResolvedObj

@dataclass(slots=True, frozen=True)
class ResolvedSystem(BaseResolvedObj[SystemState, SystemConfig]):
    pass
