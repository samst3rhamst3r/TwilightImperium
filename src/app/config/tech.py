from dataclasses import dataclass, field
from typing import Optional
from collections.abc import Sequence

from .shared.obj_ import ConfigObj
from ..types.techtype import TechType

@dataclass(frozen=True, kw_only=True, slots=True)
class Tech(ConfigObj):
    name: str
    type: Optional[TechType] = None
    pre_reqs: Sequence[TechType] = field(default_factory=tuple)
    