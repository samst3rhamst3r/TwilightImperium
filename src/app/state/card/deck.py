from dataclasses import dataclass, field
from random import shuffle
from types import MappingProxyType

from app.state.base import Serializable
from app.state.base.mixins import UUIDInstancedStateObj
from .action import ActionCardState
from .objective import PublicObjectiveCardState, SecretObjectiveCardState

class EmptyCardDeckError(Exception):
    """Raised when trying to draw from an empty card deck."""
    pass

_CLASS_TYPE_DICT_KEY = "$type"

_TYPE_REGISTRY: MappingProxyType[str, UUIDInstancedStateObj] = MappingProxyType({
    ActionCardState.__name__: ActionCardState,
    PublicObjectiveCardState.__name__: PublicObjectiveCardState,
    SecretObjectiveCardState.__name__: SecretObjectiveCardState
})

@dataclass(kw_only=True)
class CardDeckState[TCard: UUIDInstancedStateObj](Serializable):
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
        raise EmptyCardDeckError(f"Cannot draw from empty card deck")

    def discard(self, card: TCard) -> None:
        self.discard_pile.append(card)

    def save(self) -> dict:
        return super().save() | {
            "deck": [{_CLASS_TYPE_DICT_KEY: card.__class__.__name__} | card.save() for card in self.deck],
            "discard_pile": [{_CLASS_TYPE_DICT_KEY: card.__class__.__name__} | card.save() for card in self.discard_pile]
        }

    def init_from_save(self, data: dict) -> None:
        super().init_from_save(data)
        self.deck = [_TYPE_REGISTRY[card_data[_CLASS_TYPE_DICT_KEY]].load(card_data) for card_data in data["deck"]]
        self.discard_pile = [_TYPE_REGISTRY[card_data[_CLASS_TYPE_DICT_KEY]].load(card_data) for card_data in data["discard_pile"]]
