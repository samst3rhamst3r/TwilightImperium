from dataclasses import dataclass

from app.state.base import Serializable
from app.config.objs.id import IDConfigObj

@dataclass(slots=True, frozen=True)
class BaseResolvedObj[TState: Serializable, TConfig: IDConfigObj]:
    state: TState
    config: TConfig