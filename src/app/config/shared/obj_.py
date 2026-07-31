from dataclasses import dataclass
from typing import Any, Optional, get_args, get_origin, get_type_hints

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

    def __str__(self):
        return f"{self.id}"
    
@dataclass(slots=True, frozen=True, kw_only=True)
class NamedConfigObj(ConfigObj):
    """Configuration object for ID-based entities that have names."""
    name: str

    def __str__(self):
        return f"{self.name}"

@dataclass(slots=True, frozen=True, kw_only=True)
class FactionExclusiveConfigObj(NamedConfigObj):
    """Configuration object for name and ID-based entities that may have faction exclusivity."""
    faction_exclusive_id: Optional[str] = None

    def is_exclusive_to(self, faction_id: str) -> bool:
        return self.faction_exclusive_id == faction_id

    @property
    def is_faction_exclusive(self) -> bool:
        return self.faction_exclusive_id is not None