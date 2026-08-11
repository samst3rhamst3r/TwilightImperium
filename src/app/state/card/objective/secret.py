from dataclasses import dataclass
from enum import auto

from app.config.shared.enum import SerializableEnum
from app.state.base.ownable import PlayerOwnableMixin

from .base import InvalidStateTransition, ObjectiveCardState, Revealable

class SecretObjectiveZone(SerializableEnum):
    IN_DECK = auto()
    IN_HAND = auto()
    SCORED = auto()
    REVEALED = auto()

@dataclass(kw_only=True)
class SecretObjectiveCardState(ObjectiveCardState, PlayerOwnableMixin, Revealable):
    zone: SecretObjectiveZone = SecretObjectiveZone.IN_DECK

    @property
    def can_be_drawn(self) -> bool:
        return self.zone is SecretObjectiveZone.IN_DECK

    @property
    def can_be_scored(self) -> bool:
        return self.zone is SecretObjectiveZone.IN_HAND

    @property
    def can_be_revealed(self) -> bool:
        return self.zone is SecretObjectiveZone.SCORED

    @property
    def can_be_discarded(self) -> bool:
        return self.zone is SecretObjectiveZone.IN_HAND

    @property
    def is_scored(self) -> bool:
        return self.zone is SecretObjectiveZone.SCORED

    @property
    def is_revealed(self) -> bool:
        return self.zone is SecretObjectiveZone.REVEALED

    def reveal(self) -> None:
        if not self.can_be_revealed:
            raise InvalidStateTransition("This secret objective must already be scored to be revealed.")
        self.zone = SecretObjectiveZone.REVEALED

    def give_to_player(self, player_id: str) -> None:
        if self.zone is not SecretObjectiveZone.IN_DECK:
            raise InvalidStateTransition(f"Only objectives drawn from the deck can be given to a player. Current location: {self.zone.name}")
        self.ownable.assign_owner(player_id)
        self.zone = SecretObjectiveZone.IN_HAND

    def release_owner_and_score(self) -> str:
        self.zone = SecretObjectiveZone.SCORED
        return self.ownable.release_owner() # Being now scored, the reference will be stored in the player's scored_objective_card_ids list

    def release_owner_and_discard(self) -> str:
        if not self.can_be_discarded:
            raise InvalidStateTransition(f"Only objectives in hand can be discarded. Current location: {self.zone.name}")
        self.zone = SecretObjectiveZone.IN_DECK
        return self.ownable.release_owner()

    def save(self):
        return super().save() | {
            "zone": self.zone
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.zone = SecretObjectiveZone(data["zone"])
