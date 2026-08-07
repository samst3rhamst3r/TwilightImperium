from dataclasses import dataclass

from app.state.base.protocols import MixinInitializer, Savable

class AlreadyOwnedResourceException(Exception): pass
class NotYetOwnedResourceException(Exception): pass

@dataclass(slots=True, kw_only=True)
class PlayerOwnable(Savable, MixinInitializer):
    owned_by_player_id: str | None = None

    def to_save_dict(self):
        return {
            "owned_by_player_id": self.owned_by_player_id
        }

    def assign_owner(self, player_id: str) -> None:
        if self.owned_by_player_id is not None:
            raise AlreadyOwnedResourceException(f'This resource is already owned by player ID {self.owned_by_player_id}.')
        self.owned_by_player_id = player_id

    def reassign_owner(self, player_id: str) -> str:
        if self.owned_by_player_id is None:
            raise NotYetOwnedResourceException('This resource is not yet owned by any player. Cannot reassign a non-owned resource.')
        released_player_id = self.release_owner()
        self.assign_owner(player_id)
        return released_player_id

    def release_owner(self) -> str:
        if self.owned_by_player_id is None:
            raise NotYetOwnedResourceException('This resource is not yet owned by any player. Cannot release a non-owned resource.')
        released_player_id = self.owned_by_player_id
        self.owned_by_player_id = None
        return released_player_id

    @property
    def is_owned(self) -> bool:
        return self.owned_by_player_id is not None

    def is_owned_by_player(self, player_id: str) -> bool:
        return self.owned_by_player_id is not None and self.owned_by_player_id == player_id