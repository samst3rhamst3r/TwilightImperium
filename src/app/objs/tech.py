import enum
import dataclasses as dc

class TechType(enum.Enum):
    BIOTIC = enum.auto()
    WARFARE = enum.auto()
    PROPULSION = enum.auto()
    CYBERNETIC = enum.auto()

@dc.dataclass(frozen=True, slots=True)
class Tech:
    name: str
    type: TechType | None
    pre_reqs: list[TechType] | None