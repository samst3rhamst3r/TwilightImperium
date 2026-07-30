from dataclasses import dataclass, field

from app.config.shared.obj_ import ConfigObj
from app.types.agenda import AgendaType

@dataclass(slots=True, frozen=True, kw_only=True)
class AgendaCardConfig(ConfigObj):
    name: str
    type_: AgendaType = field(metadata={"key": "type"})
