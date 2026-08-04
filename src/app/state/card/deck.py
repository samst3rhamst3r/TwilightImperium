from dataclasses import dataclass, field
from random import shuffle

from .base import CardState

class EmptyCardDeckError(Exception):
    """Raised when trying to draw from an empty card deck."""
    pass

@dataclass(slots=True, kw_only=True)
class CardDeckState[TCard: CardState]:
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
    