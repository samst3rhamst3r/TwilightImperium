from dataclasses import dataclass, field
from typing import ClassVar, Protocol

from app.errors import GameError

from .serializable import Serializable

class OwnershipError(GameError):
    entity_name: ClassVar[str] = "resource"

    def __init__(self, entity_id: str, actual_owner_id: str | None):
        super().__init__(
            f"{self.entity_name.capitalize()} {entity_id!r} is not owned by the requesting player "
            f"(owned by {actual_owner_id!r})"
        )

class AlreadyOwnedResourceException(Exception):
    """Raised when trying to assign ownership of a resource that is already owned by another player."""

class NotYetOwnedResourceException(Exception):
    """Raised when trying to release ownership of a resource that is not yet
    owned by any player. Unlike OwnershipError's other uses (a requesting
    player vs. actual-owner mismatch), there is no "actual owner" to report
    here, so this overrides OwnershipError's two-argument __init__ instead
    of inheriting it."""

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

    def set_owner(self, player_id: str) -> None:
        self.owned_by_player_id = player_id

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

class OwnableEntity(Protocol):
    """This Protocol is used to provide a common interface for all entities that are ownable by a player."""
    ownable: _PlayerOwnable

    @property
    def id(self) -> str: ...
