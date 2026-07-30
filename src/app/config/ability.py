from dataclasses import dataclass, field
from collections.abc import Mapping
from typing import Any

from .shared.obj_ import ConfigRefObj

@dataclass(slots=True, frozen=True, kw_only=True)
class AbilityRefConfig(ConfigRefObj):
    kwargs: Mapping[str, Any] = field(default_factory=dict)
