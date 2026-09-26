from dataclasses import dataclass

from ..fromdict import BaseConfigObj

@dataclass(frozen=True, kw_only=True)
class IDConfigObj(BaseConfigObj):
    """Configuration object for ID-based entities."""
    id: str

    def __str__(self):
        return f"{self.id}"
    