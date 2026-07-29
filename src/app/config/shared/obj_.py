from dataclasses import dataclass
from typing import Any, get_args, get_origin, get_type_hints

@dataclass(slots=True, frozen=True, kw_only=True)
class BaseConfigObj:
    """Base class for all configuration objects."""

    @classmethod
    def from_raw_config(cls, raw_data: Any):
        pass

@dataclass(slots=True, frozen=True, kw_only=True)
class ConfigObj(BaseConfigObj):
    """Configuration object for ID-based entities."""
    id: str

@dataclass(slots=True, frozen=True, kw_only=True)
class ConfigRefObj(BaseConfigObj):
    """Configuration object for referencing other configuration objects."""
    ref_id: str
