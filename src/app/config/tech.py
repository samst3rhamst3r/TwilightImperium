from dataclasses import dataclass, field
from typing import Optional
from collections.abc import Sequence

from .shared.obj_ import ConfigObj
from .tech_req import TechReqConfig
from ..types.tech_type import TechType

@dataclass(frozen=True, kw_only=True, slots=True)
class TechConfig(ConfigObj):
    name: str
    tech_type: TechType
    prereqs: Optional[Sequence[TechReqConfig]] = field(default_factory=tuple)
    