from dataclasses import dataclass

from app.state.base import BaseStateObj
from app.config.shared import BaseConfigObj

@dataclass(slots=True, frozen=True)
class BaseResolvedObj[TState: BaseStateObj, TConfig: BaseConfigObj]:
    state: TState
    config: TConfig