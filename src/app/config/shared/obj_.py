from dataclasses import dataclass
from abc import ABC
from typing import Any, get_args, get_origin, get_type_hints

@dataclass(frozen=True, kw_only=True, slots=True)
class ConfigObj(ABC):
    """Base class for all configuration objects."""
    id: str

    @classmethod
    def from_raw_config(cls, raw_data: Any):
        pass