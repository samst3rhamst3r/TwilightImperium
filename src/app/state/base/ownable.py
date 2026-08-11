from dataclasses import dataclass, field
from typing import Protocol

from .serializable import Serializable

class AlreadyOwnedResourceException(Exception): 
    pass
class NotYetOwnedResourceException(Exception): 
    pass

@dataclass(kw_only=True)
class _PlayerOwnable(Serializable):
    """Contains the state logic regarding validation of player ownership of a resource.
    
    The other classes in this module allow for semantic distinction between various classes.
    While some classes "assign_owner", a Planet "assigns control". This semantic uniqueness means
    there needs to be a functional redirect that uses terminology that is self-documenting.

    Classes that typically use "owner"-type language can leverage the convenience Protocol in this module
    to inherit such methods. Other classes, like PlanetObjects will instantiate their own unique
    vocabulary that forwards through the contained "PlayerOwnableMixin" class to the resolved generic "owner"
    functionality semantics.

    In other words:
    For "owner" semantics
        calling entity -> "assign_owner" is called on inherited protocol -> protocol forwards through PlayerOwnable -> assign_owner on _PlayerOwnable

    For "control" semantics
        calling entity -> "assign_control" is called on the leaf class -> leaf class implements forwarding to PlayerOwnable -> assign_owner on _PlayerOwnable
    """
    owned_by_player_id: str | None = None

    def save(self):
        return super().save() | {
            "owned_by_player_id": self.owned_by_player_id
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.owned_by_player_id = data["owned_by_player_id"]

    def assign_owner(self, player_id: str) -> None:
        if self.is_owned:
            raise AlreadyOwnedResourceException(f'This resource is already owned by player ID {self.owned_by_player_id}.')
        self.owned_by_player_id = player_id

    def reassign_owner(self, player_id: str) -> str:
        if not self.is_owned:
            raise NotYetOwnedResourceException('This resource is not yet owned by any player. Cannot reassign a non-owned resource.')
        released_player_id = self.release_owner()
        self.assign_owner(player_id)
        return released_player_id

    def release_owner(self) -> str:
        if not self.is_owned:
            raise NotYetOwnedResourceException('This resource is not yet owned by any player. Cannot release ownership of a non-owned resource.')
        released_player_id = self.owned_by_player_id
        self.owned_by_player_id = None
        return released_player_id

    @property
    def is_owned(self) -> bool:
        return self.owned_by_player_id is not None

    def is_owned_by_player(self, player_id: str) -> bool:
        return self.is_owned and self.owned_by_player_id == player_id

@dataclass(kw_only=True)
class PlayerOwnableMixin(Serializable):
    """This Mixin provides one layer of indirection to enable semantically distinct but functionally similar objects.
    
    Together with the _PlayerAssignableConvenienceProtocol, calling entities can inherit common functionality. If
    unique semantics are desired per class, the Convenience Protocol cannot be used - recommendation is to implement
    unique semantics on the bespoke leaf class.

    e.g. "assign_speaker" will get functionally equivalent usage as "assign_owner" in the convenience Protocol.
    """
    ownable: _PlayerOwnable = field(default_factory=_PlayerOwnable)

    def save(self) -> dict:
        return super().save() | {
            "ownable": self.ownable.save()
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.ownable = _PlayerOwnable.load(data["ownable"])

class _PlayerAssignableConvenienceProtocol(Protocol):
    ownable: _PlayerOwnable

    def assign_owner(self, player_id: str) -> None:
        self.ownable.assign_owner(player_id)

    def reassign_owner(self, player_id: str) -> str:
        return self.ownable.reassign_owner(player_id)

    def release_owner(self) -> str:
        return self.ownable.release_owner()

    @property
    def is_owned(self) -> bool:
        return self.ownable.is_owned

    def is_owned_by_player(self, player_id: str) -> bool:
        return self.ownable.is_owned_by_player(player_id)

class PlayerOwnableWithConvenienceProtocol(PlayerOwnableMixin, _PlayerAssignableConvenienceProtocol):
    pass