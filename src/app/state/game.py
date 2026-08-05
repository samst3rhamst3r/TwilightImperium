from dataclasses import dataclass

from .base import BaseStateObj

from .map import MapState
from .planet import PlanetState
from .player import PlayerState
from .system import SystemState
from .unit import UnitState
from .special_tokens import NaaluTokenState, NekroAssimilatorTokenState, CreussWormholeTokenState, SpeakerTokenState

from .card import CardDeckState, PublicObjectiveCardState, SecretObjectiveCardState, ActionCardState, PromissoryNoteCardState, StrategyCardState

@dataclass(slots=True, kw_only=True)
class GameState(BaseStateObj):
    players: tuple[PlayerState, ...]
    map: MapState
    speaker_token: SpeakerTokenState
    systems: tuple[SystemState, ...]
    planets: tuple[PlanetState, ...]

    strategy_cards: list[StrategyCardState]
    promissory_notes: list[PromissoryNoteCardState]
    revealed_public_objectives: list[PublicObjectiveCardState]

    # Card decks
    public_objective_i_deck: CardDeckState[PublicObjectiveCardState]
    public_objective_ii_deck: CardDeckState[PublicObjectiveCardState]
    secret_objective_deck: CardDeckState[SecretObjectiveCardState]
    action_card_deck: CardDeckState[ActionCardState]

    # Special tokens, only used with particular factions
    naalu_token: NaaluTokenState | None = None
    nekro_assimilator_tokens: tuple[NekroAssimilatorTokenState, NekroAssimilatorTokenState] | None = None
    creuss_wormhole_token: CreussWormholeTokenState | None = None

    def to_save_dict(self) -> dict:
        return {
            "players": [player.to_save_dict() for player in self.players],
            "map": self.map.to_save_dict(),
            "speaker_token": self.speaker_token.to_save_dict(),
            "systems": [system.to_save_dict() for system in self.systems],
            "planets": [planet.to_save_dict() for planet in self.planets],
            "strategy_cards": [card.to_save_dict() for card in self.strategy_cards],
            "promissory_notes": [card.to_save_dict() for card in self.promissory_notes],
            "revealed_public_objectives": [card.to_save_dict() for card in self.revealed_public_objectives],
            "public_objective_i_deck": self.public_objective_i_deck.to_save_dict(),
            "public_objective_ii_deck": self.public_objective_ii_deck.to_save_dict(),
            "secret_objective_deck": self.secret_objective_deck.to_save_dict(),
            "action_card_deck": self.action_card_deck.to_save_dict(),
            "naalu_token": self.naalu_token.to_save_dict() if self.naalu_token else None,
            "nekro_assimilator_tokens": [token.to_save_dict() for token in self.nekro_assimilator_tokens] if self.nekro_assimilator_tokens else None,
            "creuss_wormhole_token": self.creuss_wormhole_token.to_save_dict() if self.creuss_wormhole_token else None,
        }

    @classmethod
    def from_save_dict(cls, data: dict):
        return cls(
            players=[PlayerState.from_save_dict(player_data) for player_data in data["players"]],
            map=MapState.from_save_dict(data["map"]),
            speaker_token=SpeakerTokenState.from_save_dict(data["speaker_token"]),
            systems=[SystemState.from_save_dict(system_data) for system_data in data["systems"]],
            planets=[PlanetState.from_save_dict(planet_data) for planet_data in data["planets"]],
            strategy_cards=[StrategyCardState.from_save_dict(card_data) for card_data in data["strategy_cards"]],
            promissory_notes=[PromissoryNoteCardState.from_save_dict(card_data) for card_data in data["promissory_notes"]],
            revealed_public_objectives=[PublicObjectiveCardState.from_save_dict(card_data) for card_data in data["revealed_public_objectives"]],
            public_objective_i_deck=CardDeckState[PublicObjectiveCardState].from_save_dict(data["public_objective_i_deck"]),
            public_objective_ii_deck=CardDeckState[PublicObjectiveCardState].from_save_dict(data["public_objective_ii_deck"]),
            secret_objective_deck=CardDeckState[SecretObjectiveCardState].from_save_dict(data["secret_objective_deck"]),
            action_card_deck=CardDeckState[ActionCardState].from_save_dict(data["action_card_deck"]),
            naalu_token=NaaluTokenState.from_save_dict(data["naalu_token"]) if data["naalu_token"] else None,
            nekro_assimilator_tokens=(NekroAssimilatorTokenState.from_save_dict(data["nekro_assimilator_tokens"][0]), NekroAssimilatorTokenState.from_save_dict(data["nekro_assimilator_tokens"][1])) if data["nekro_assimilator_tokens"] else None,
            creuss_wormhole_token=CreussWormholeTokenState.from_save_dict(data["creuss_wormhole_token"]) if data["creuss_wormhole_token"] else None,
        )