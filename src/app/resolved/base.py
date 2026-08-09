from dataclasses import dataclass

from app.state.base import Serializable
from app.config.shared import BaseConfigObj

@dataclass(slots=True, frozen=True)
class BaseResolvedObj[TState: Serializable, TConfig: BaseConfigObj]:
    state: TState
    config: TConfig