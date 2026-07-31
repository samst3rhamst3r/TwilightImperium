from dataclasses import dataclass, field
from typing import Optional
from collections.abc import Sequence

from ..shared import ConfigObj
from .upgrade_req import TechUpgradeReqConfig
from .type import TechType

@dataclass(frozen=True, kw_only=True, slots=True)
class TechConfig(ConfigObj):
    name: str
    tech_type: TechType
    prereqs: Optional[Sequence[TechUpgradeReqConfig]] = field(default_factory=tuple)
    