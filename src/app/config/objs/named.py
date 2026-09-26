from dataclasses import dataclass

from .id import IDConfigObj

@dataclass(frozen=True, kw_only=True)
class NamedConfigObj(IDConfigObj):
    """Configuration object for ID-based entities that have names."""
    name: str

    def __str__(self):
        return f"{self.name}"

