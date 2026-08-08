from collections.abc import Iterable
from dataclasses import dataclass
from types import MappingProxyType

from .base import StateObj

from .planet import PlanetState
from .player import PlayerState
from .system import SystemState
from .unit import UnitState
from .special_tokens import NaaluTokenState, NekroAssimilatorTokenState, CreussWormholeTokenState, SpeakerTokenState

from .card import CardDeckState, PublicObjectiveCardState, SecretObjectiveCardState, ActionCardState, PromissoryNoteCardState, StrategyCardState

@dataclass(slots=True, kw_only=True)
class GameState(StateObj):
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
    creuss_wormhole_tokens: tuple[CreussWormholeTokenState, CreussWormholeTokenState] = ()

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

    def to_save_dict(self) -> dict:
        return {
            "players": [player.to_save_dict() for player in self.players.values()],
            "speaker_token": self.speaker_token.to_save_dict(),
            "systems": [system.to_save_dict() for system in self.systems.values()],
            "planets": [planet.to_save_dict() for planet in self.planets.values()],
            "deployed_units": [unit.to_save_dict() for unit in self.deployed_units.values()],
            "strategy_cards": [card.to_save_dict() for card in self.strategy_cards.values()],
            "promissory_notes": [card.to_save_dict() for card in self.promissory_notes.values()],
            "revealed_public_objectives": [card.to_save_dict() for card in self.revealed_public_objectives.values()],
            "public_objective_i_deck": self.public_objective_i_deck.to_save_dict(),
            "public_objective_ii_deck": self.public_objective_ii_deck.to_save_dict(),
            "secret_objective_deck": self.secret_objective_deck.to_save_dict(),
            "action_card_deck": self.action_card_deck.to_save_dict(),
            "naalu_token": self.naalu_token.to_save_dict() if self.naalu_token else None,
            "nekro_assimilator_tokens": {token["id"]: token.to_save_dict() for token in self.nekro_assimilator_tokens.values()} if self.nekro_assimilator_tokens else None,
            "creuss_wormhole_token": self.creuss_wormhole_token.to_save_dict() if self.creuss_wormhole_token else None
        }

    def init_from_save(self, data: dict):
        self.players =                      {id: PlayerState.from_save_dict(player_data) for id, player_data in data["players"].items()}
        self.systems =                      {id: SystemState.from_save_dict(system_data) for id, system_data in data["systems"].items()}
        self.planets =                      {id: PlanetState.from_save_dict(planet_data) for id, planet_data in data["planets"].items()}
        self.speaker_token =                SpeakerTokenState.from_save_dict(data["speaker_token"])
        self.strategy_cards =               {id: StrategyCardState.from_save_dict(card_data) for id, card_data in data["strategy_cards"].items()}
        self.promissory_notes =             {id: PromissoryNoteCardState.from_save_dict(card_data) for id, card_data in data["promissory_notes"].items()}
        self.revealed_public_objectives =   {id: PublicObjectiveCardState.from_save_dict(card_data) for id, card_data in data["revealed_public_objectives"].items()}
        self.public_objective_i_deck =      CardDeckState[PublicObjectiveCardState].from_save_dict(data["public_objective_i_deck"])
        self.public_objective_ii_deck =     CardDeckState[PublicObjectiveCardState].from_save_dict(data["public_objective_ii_deck"])
        self.secret_objective_deck =        CardDeckState[SecretObjectiveCardState].from_save_dict(data["secret_objective_deck"])
        self.action_card_deck =             CardDeckState[ActionCardState].from_save_dict(data["action_card_deck"])
        self.naalu_token =                  NaaluTokenState.from_save_dict(data["naalu_token"])
        self.nekro_assimilator_tokens =     {token["id"]: NekroAssimilatorTokenState.from_save_dict(token) for token in data["nekro_assimilator_tokens"].values()}
        self.creuss_wormhole_token =        CreussWormholeTokenState.from_save_dict(data["creuss_wormhole_token"])

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

