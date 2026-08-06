from collections.abc import Iterable
from dataclasses import dataclass
from turtle import st
from types import MappingProxyType

from .base import BaseStateObj

from .planet import PlanetState
from .player import PlayerState
from .system import SystemState
from .unit import UnitState
from .special_tokens import NaaluTokenState, NekroAssimilatorTokenState, CreussWormholeTokenState, SpeakerTokenState

from .card import CardDeckState, PublicObjectiveCardState, SecretObjectiveCardState, ActionCardState, PromissoryNoteCardState, StrategyCardState

@dataclass(slots=True, kw_only=True)
class GameState(BaseStateObj):
    players: MappingProxyType[str, PlayerState]
    systems: MappingProxyType[str, SystemState]
    planets: MappingProxyType[str, PlanetState]
    speaker_token: SpeakerTokenState
    deployed_units: dict[str, UnitState]

    strategy_cards: MappingProxyType[str, StrategyCardState]
    promissory_notes: MappingProxyType[str, PromissoryNoteCardState]
    revealed_public_objectives: dict[str, PublicObjectiveCardState]

    # Card decks
    public_objective_i_deck: CardDeckState[PublicObjectiveCardState]
    public_objective_ii_deck: CardDeckState[PublicObjectiveCardState]
    secret_objective_deck: CardDeckState[SecretObjectiveCardState]
    action_card_deck: CardDeckState[ActionCardState]

    # Special tokens, only used with particular factions
    naalu_token: NaaluTokenState | None = None
    nekro_assimilator_tokens: MappingProxyType[str, NekroAssimilatorTokenState] | None = None
    creuss_wormhole_token: CreussWormholeTokenState | None = None

    @classmethod
    def new_game(
            cls, 
            players: Iterable[PlayerState],
            systems: Iterable[SystemState],
            planets: Iterable[PlanetState],
            speaker_player_id: str,

        ):
        return cls(
            players={},
            speaker_token=SpeakerTokenState(),
            systems={},
            planets={},
            deployed_units={},
            strategy_cards={},
            promissory_notes={},
            revealed_public_objectives={},
            public_objective_i_deck=CardDeckState[PublicObjectiveCardState](),
            public_objective_ii_deck=CardDeckState[PublicObjectiveCardState](),
            secret_objective_deck=CardDeckState[SecretObjectiveCardState](),
            action_card_deck=CardDeckState[ActionCardState](),
        )

    @classmethod
    def from_save_dict(cls, data: dict):
        return cls(
            players={player_data["id"]: PlayerState.from_save_dict(player_data) for player_data in data["players"]},
            speaker_token=SpeakerTokenState.from_save_dict(data["speaker_token"]),
            systems={system_data["id"]: SystemState.from_save_dict(system_data) for system_data in data["systems"]},
            planets={planet_data["id"]: PlanetState.from_save_dict(planet_data) for planet_data in data["planets"]},
            strategy_cards={card_data["id"]: StrategyCardState.from_save_dict(card_data) for card_data in data["strategy_cards"]},
            promissory_notes={card_data["id"]: PromissoryNoteCardState.from_save_dict(card_data) for card_data in data["promissory_notes"]},
            revealed_public_objectives={card_data["id"]: PublicObjectiveCardState.from_save_dict(card_data) for card_data in data["revealed_public_objectives"]},
            public_objective_i_deck=CardDeckState[PublicObjectiveCardState].from_save_dict(data["public_objective_i_deck"]),
            public_objective_ii_deck=CardDeckState[PublicObjectiveCardState].from_save_dict(data["public_objective_ii_deck"]),
            secret_objective_deck=CardDeckState[SecretObjectiveCardState].from_save_dict(data["secret_objective_deck"]),
            action_card_deck=CardDeckState[ActionCardState].from_save_dict(data["action_card_deck"]),
            naalu_token=NaaluTokenState.from_save_dict(data["naalu_token"]) if data["naalu_token"] else None,
            nekro_assimilator_tokens={token["id"]: NekroAssimilatorTokenState.from_save_dict(token) for token in data["nekro_assimilator_tokens"].values()} if data["nekro_assimilator_tokens"] else None,
            creuss_wormhole_token=CreussWormholeTokenState.from_save_dict(data["creuss_wormhole_token"]) if data["creuss_wormhole_token"] else None,
        )

    def to_save_dict(self) -> dict:
        return {
            "players": {player.id: player.to_save_dict() for player in self.players.values()},
            "speaker_token": self.speaker_token.to_save_dict(),
            "systems": {system.id: system.to_save_dict() for system in self.systems.values()},
            "planets": {planet.id: planet.to_save_dict() for planet in self.planets.values()},
            "deployed_units": {unit.id: unit.to_save_dict() for unit in self.deployed_units.values()},
            "strategy_cards": {card.id: card.to_save_dict() for card in self.strategy_cards.values()},
            "promissory_notes": {card.id: card.to_save_dict() for card in self.promissory_notes.values()},
            "revealed_public_objectives": {card.id: card.to_save_dict() for card in self.revealed_public_objectives.values()},
            "public_objective_i_deck": self.public_objective_i_deck.to_save_dict(),
            "public_objective_ii_deck": self.public_objective_ii_deck.to_save_dict(),
            "secret_objective_deck": self.secret_objective_deck.to_save_dict(),
            "action_card_deck": self.action_card_deck.to_save_dict(),
            "naalu_token": self.naalu_token.to_save_dict() if self.naalu_token else None,
            "nekro_assimilator_tokens": {token.id: token.to_save_dict() for token in self.nekro_assimilator_tokens.values()} if self.nekro_assimilator_tokens else None,
            "creuss_wormhole_token": self.creuss_wormhole_token.to_save_dict() if self.creuss_wormhole_token else None,
        }

