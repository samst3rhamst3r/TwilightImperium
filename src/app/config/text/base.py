from dataclasses import dataclass

from app.config.base import ConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class BaseTextConfigObj(ConfigObj):
    """Base class for all text configurations. Used by type-checkers."""
    pass
