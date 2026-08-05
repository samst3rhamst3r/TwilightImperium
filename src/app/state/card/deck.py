from dataclasses import dataclass, field
from random import shuffle
from typing import Self
from collections.abc import Iterable

from app.state.base import BaseStateObj
from .base import CardState

class EmptyCardDeckError(Exception):
    """Raised when trying to draw from an empty card deck."""
    pass

@dataclass(slots=True, kw_only=True)
class CardDeckState[TCard: CardState](BaseStateObj):
    deck: list[TCard]
    discard_pile: list[TCard] = field(default_factory=list)

    def shuffle_deck(self) -> None:
        shuffle(self.deck)

    def shuffle_discard_pile_back_into_deck(self) -> None:
        if self.discard_pile:
            self.deck.extend(self.discard_pile)
            self.discard_pile.clear()
            self.shuffle_deck()

    def draw(self) -> TCard:
        if self.deck:
            return self.deck.pop()
        raise EmptyCardDeckError(f"Cannot draw from empty {TCard.__name__} card deck")

    def discard(self, card: TCard) -> None:
        self.discard_pile.append(card)

    def to_save_dict(self):
        return {
            "deck": [card.to_save_dict() for card in self.deck],
            "discard_pile": [card.to_save_dict() for card in self.discard_pile]
        }

    @classmethod
    def from_save_dict(cls, deck: Iterable[TCard], discard_pile: Iterable[TCard], **kwargs) -> Self:
        return cls(
            deck=list(deck),
            discard_pile=list(discard_pile),
            **kwargs
        )