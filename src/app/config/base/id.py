from dataclasses import dataclass

from .base import BaseConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class ConfigObj(BaseConfigObj):
    """Configuration object for ID-based entities."""
    id: str

    def __str__(self):
        return f"{self.id}"
    