from dataclasses import dataclass

from app.state.base import StateObj
from app.config.shared import BaseConfigObj

@dataclass(slots=True, frozen=True)
class BaseResolvedObj[TState: StateObj, TConfig: BaseConfigObj]:
    state: TState
    config: TConfig