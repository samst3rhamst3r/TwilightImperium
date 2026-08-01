from dataclasses import dataclass

from app.config.base import FactionExclusiveConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class PromissoryNoteConfig(FactionExclusiveConfigObj):
    """Config for a promissory note."""
    pass