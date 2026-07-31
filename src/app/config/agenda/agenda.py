from dataclasses import dataclass, field

from app.config.shared import NamedConfigObj

from .type import AgendaType

@dataclass(slots=True, frozen=True, kw_only=True)
class AgendaConfig(NamedConfigObj):
    type_: AgendaType = field(metadata={"key": "type"})
