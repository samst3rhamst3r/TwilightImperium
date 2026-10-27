from dataclasses import dataclass

from app.state.objs import UUIDInstancedStateObj, Exhaustible

@dataclass(kw_only=True)
class TechCardState(UUIDInstancedStateObj, Exhaustible):
    pass
