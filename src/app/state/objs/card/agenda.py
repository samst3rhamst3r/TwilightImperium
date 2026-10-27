from dataclasses import dataclass

from app.state.objs import ConfigIDStateObj, Exhaustible

@dataclass(kw_only=True)
class AgendaCardState(ConfigIDStateObj, Exhaustible):
    pass
