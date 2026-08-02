from dataclasses import dataclass

from .named import NamedConfigObj

@dataclass(slots=True, frozen=True, kw_only=True)
class CanHaveFactionExclusivity(NamedConfigObj):
    """Configuration object for name and ID-based entities that may have faction exclusivity."""
    faction_exclusive_id: str | None = None

    def is_exclusive_to(self, faction_id: str) -> bool:
        return self.faction_exclusive_id == faction_id

    @property
    def is_faction_exclusive(self) -> bool:
        return self.faction_exclusive_id is not None