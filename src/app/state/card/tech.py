from dataclasses import dataclass

from app.state.base.exhaustible import Exhaustible
from app.state.base.mixins import UUIDInstancedStateObj

@dataclass(kw_only=True)
class TechCardState(UUIDInstancedStateObj, Exhaustible):
    pass
