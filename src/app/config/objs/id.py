from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class IDConfigObj:
    """Configuration object for ID-based entities."""
    id: str

    def __str__(self):
        return f"{self.id}"
    