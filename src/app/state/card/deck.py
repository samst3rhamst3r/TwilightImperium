from dataclasses import dataclass, field
from random import shuffle

from app.state.base import Serializable

class EmptyCardDeckError(Exception):
    """Raised when trying to draw from an empty card deck."""
    pass

@dataclass(kw_only=True)
class CardDeckState(Serializable):
    deck: list[str]
    discard_pile: list[str] = field(default_factory=list)

    def shuffle_deck(self) -> None:
        shuffle(self.deck)

    def shuffle_discard_pile_back_into_deck(self) -> None:
        if self.discard_pile:
            self.deck.extend(self.discard_pile)
            self.discard_pile.clear()
            self.shuffle_deck()

    def draw(self) -> str:
        if self.deck:
            return self.deck.pop()
        raise EmptyCardDeckError(f"Cannot draw from empty card deck")

    def discard(self, card_id: str) -> None:
        self.discard_pile.append(card_id)

    def save(self) -> dict:
        return super().save() | {
            "deck": self.deck,
            "discard_pile": self.discard_pile
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.deck = data["deck"]
        self.discard_pile = data["discard_pile"]
