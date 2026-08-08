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

    def init_from_save(self, data: dict):
        super().init_from_save(data)
        
        self.players =                      {id: PlayerState.from_save_dict(player_data) for id, player_data in data["players"].items()}
        self.systems =                      {id: SystemState.from_save_dict(system_data) for id, system_data in data["systems"].items()}
        self.planets =                      {id: PlanetState.from_save_dict(planet_data) for id, planet_data in data["planets"].items()}
        self.speaker_token =                SpeakerTokenState.from_save_dict(data["speaker_token"])
        self.deployed_units =               {id: UnitState.from_save_dict(unit_data) for id, unit_data in data["deployed_units"].items()}
        self.strategy_cards =               {id: StrategyCardState.from_save_dict(card_data) for id, card_data in data["strategy_cards"].items()}
        self.promissory_notes =             {id: PromissoryNoteCardState.from_save_dict(card_data) for id, card_data in data["promissory_notes"].items()}
        self.revealed_public_objectives =   {id: PublicObjectiveCardState.from_save_dict(card_data) for id, card_data in data["revealed_public_objectives"].items()}
        self.public_objective_i_deck =      CardDeckState[PublicObjectiveCardState].from_save_dict(data["public_objective_i_deck"])
        self.public_objective_ii_deck =     CardDeckState[PublicObjectiveCardState].from_save_dict(data["public_objective_ii_deck"])
        self.secret_objective_deck =        CardDeckState[SecretObjectiveCardState].from_save_dict(data["secret_objective_deck"])
        self.action_card_deck =             CardDeckState[ActionCardState].from_save_dict(data["action_card_deck"])
        self.naalu_token =                  NaaluTokenState.from_save_dict(data["naalu_token"])
        self.nekro_assimilator_tokens =     {token["id"]: NekroAssimilatorTokenState.from_save_dict(token) for token in data["nekro_assimilator_tokens"].values()}
        self.creuss_wormhole_tokens =       tuple(CreussWormholeTokenState.from_save_dict(token) for token in data["creuss_wormhole_tokens"])

    def to_save_dict(self) -> dict:
        return super().to_save_dict() | {
            "players": {id: player.to_save_dict() for id, player in self.players.items()},
            "systems": {id: system.to_save_dict() for id, system in self.systems.items()},
            "planets": {id: planet.to_save_dict() for id, planet in self.planets.items()},
            "speaker_token": self.speaker_token.to_save_dict(),
            "deployed_units": {id: unit.to_save_dict() for id, unit in self.deployed_units.items()},
            "strategy_cards": {id: card.to_save_dict() for id, card in self.strategy_cards.items()},
            "promissory_notes": {id: card.to_save_dict() for id, card in self.promissory_notes.items()},
            "revealed_public_objectives": {id: card.to_save_dict() for id, card in self.revealed_public_objectives.items()},
            "public_objective_i_deck": self.public_objective_i_deck.to_save_dict(),
            "public_objective_ii_deck": self.public_objective_ii_deck.to_save_dict(),
            "secret_objective_deck": self.secret_objective_deck.to_save_dict(),
            "action_card_deck": self.action_card_deck.to_save_dict(),
            "naalu_token": self.naalu_token.to_save_dict() if self.naalu_token else None,
            "nekro_assimilator_tokens": {token.id: token.to_save_dict() for token in self.nekro_assimilator_tokens.values()} if self.nekro_assimilator_tokens else None,
            "creuss_wormhole_tokens": [token.to_save_dict() for token in self.creuss_wormhole_tokens]
        }

