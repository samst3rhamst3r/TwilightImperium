from typing import Protocol

from app.config.shared import RequiresFunctionalText, RequiresFlavorText, RequiresFlavorTextOptions, CanHaveFactionExclusivity

class ResolvedFunctionalTextMixin(Protocol):
    config: RequiresFunctionalText

    @property
    def functional_text(self) -> str:
        return self.config.functional_text

class ResolvedFlavorTextMixin(Protocol):
    config: RequiresFlavorText

    @property
    def flavor_text(self) -> str:
        return self.config.flavor_text

class HasFlavorTextIndex(Protocol):
    flavor_text_index: int

class ResolvedFlavorTextOptionsMixin(Protocol):
    state: HasFlavorTextIndex
    config: RequiresFlavorTextOptions

    @property
    def flavor_text(self) -> str:
        return self.config.flavor_text_options[self.state.flavor_text_index]

class CanHaveFactionExclusivityMixin(Protocol):
    config: CanHaveFactionExclusivity

    def is_exclusive_to(self, faction_id: str) -> bool:
        return self.config.faction_exclusive_id == faction_id

    @property
    def is_faction_exclusive(self) -> bool:
        return self.config.faction_exclusive_id is not None