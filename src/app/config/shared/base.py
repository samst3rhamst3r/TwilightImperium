from dataclasses import dataclass
from typing import Any, get_args, get_origin, get_type_hints

@dataclass(init=False, slots=True, frozen=True)
class BaseConfigObj:
    """Base class for all configuration objects."""

    @classmethod
    def from_raw_config(cls, raw_data: Any):

        type_hints = get_type_hints(cls)
