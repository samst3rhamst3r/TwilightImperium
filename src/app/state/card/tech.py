from dataclasses import dataclass

from app.state.base.exhaustible import Exhaustible
from app.state.base.mixins import ConfigIDStateObj

@dataclass(slots=True, kw_only=True)
class TechCardState(ConfigIDStateObj, Exhaustible):
    pass
