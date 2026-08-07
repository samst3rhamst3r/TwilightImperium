from typing import Protocol

from app.config.shared import RequiresFunctionalText, RequiresFlavorText, RequiresFlavorTextOptions, CanHaveFactionExclusivity
from app.state.base import Exhaustable, PlayerOwnable

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

    @property
    def is_faction_exclusive(self) -> bool:
        return self.config.is_faction_exclusive

    def is_exclusive_to(self, faction_id: str) -> bool:
        return self.config.is_exclusive_to(faction_id)

class ExhaustableMixin(Protocol):
    config: Exhaustable

    def exhaust(self):
        self.config.exhaust()

    def ready(self):
        self.config.ready()

class PlayerOwnableMixin(Protocol):
    config: PlayerOwnable

    def assign_owner(self, player_id: str) -> None:
        self.config.assign_owner(player_id)

    def reassign_owner(self, player_id: str) -> str:
        self.config.reassign_owner(player_id)

    def release_owner(self) -> str:
        self.config.release_owner()

    @property
    def is_owned(self) -> bool:
        return self.config.is_owned

    def is_owned_by_player(self, player_id: str) -> bool:
        return self.config.is_owned_by_player(player_id)