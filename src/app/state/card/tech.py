from dataclasses import dataclass

from app.state.base.state_obj import ConfigBoundStateObj

@dataclass(slots=True, kw_only=True)
class TechnologyCardState(ConfigBoundStateObj):
    pass
