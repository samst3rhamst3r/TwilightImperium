from dataclasses import dataclass

from app.config.shared import IDConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class BaseTextConfigObj(IDConfigObj):
    """Base class for all text configurations. Used by type-checkers."""
    pass
