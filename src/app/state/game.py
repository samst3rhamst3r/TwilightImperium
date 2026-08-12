from dataclasses import dataclass
from types import MappingProxyType
from typing import Self

from .base import Serializable

from .planet import PlanetState
from .player import PlayerState
from .system import SystemState
from .unit import UnitState
from .special_tokens import (
    NaaluTokenState,
    NekroAssimilatorTokenState,
    CreussWormholeTokenState,
    SpeakerTokenState,
    CustodiansTokenState,
)

from .card import (
    CardDeckState,
    PublicObjectiveCardState,
    SecretObjectiveCardState,
    ActionCardState,
    PromissoryNoteCardState,
    StrategyCardState,
    AgendaCardState,
    TechCardState,
)

@dataclass(kw_only=True)
class GameState(Serializable):
    players: MappingProxyType[str, PlayerState]
    systems: MappingProxyType[str, SystemState]
    planets: MappingProxyType[str, PlanetState]
    speaker_token: SpeakerTokenState
    custodians_token: CustodiansTokenState
    deployed_units: dict[str, UnitState]

    strategy_cards: MappingProxyType[str, StrategyCardState]
    promissory_notes: MappingProxyType[str, PromissoryNoteCardState]
    revealed_public_objectives: dict[str, PublicObjectiveCardState]

    # Agenda/Tech cards that have (or can have) mutable exhaustion state -
    # see specs/STATE_OBJS.md Open Questions for sparse-vs-dense population.
    agenda_cards: MappingProxyType[str, AgendaCardState]
    tech_cards: MappingProxyType[str, TechCardState]

    # Card decks
    public_objective_i_deck: CardDeckState[PublicObjectiveCardState]
    public_objective_ii_deck: CardDeckState[PublicObjectiveCardState]
    secret_objective_deck: CardDeckState[SecretObjectiveCardState]
    action_card_deck: CardDeckState[ActionCardState]

    # Special tokens - only present when the relevant faction (Naalu/Nekro/Creuss)
    # is in play this game.
    naalu_token: NaaluTokenState | None = None
    nekro_assimilator_tokens: tuple[NekroAssimilatorTokenState, NekroAssimilatorTokenState] | None = None
    creuss_wormhole_tokens: tuple[CreussWormholeTokenState, CreussWormholeTokenState] | None = None

    def save(self) -> dict:
        return super().save() | {
            "players": {id: player.save() for id, player in self.players.items()},
            "systems": {id: system.save() for id, system in self.systems.items()},
            "planets": {id: planet.save() for id, planet in self.planets.items()},
            "speaker_token": self.speaker_token.save(),
            "custodians_token": self.custodians_token.save(),
            "deployed_units": {id: unit.save() for id, unit in self.deployed_units.items()},
            "strategy_cards": {id: card.save() for id, card in self.strategy_cards.items()},
            "promissory_notes": {id: card.save() for id, card in self.promissory_notes.items()},
            "revealed_public_objectives": {id: card.save() for id, card in self.revealed_public_objectives.items()},
            "agenda_cards": {id: card.save() for id, card in self.agenda_cards.items()},
            "tech_cards": {id: card.save() for id, card in self.tech_cards.items()},
            "public_objective_i_deck": self.public_objective_i_deck.save(),
            "public_objective_ii_deck": self.public_objective_ii_deck.save(),
            "secret_objective_deck": self.secret_objective_deck.save(),
            "action_card_deck": self.action_card_deck.save(),
            "naalu_token": self.naalu_token.save() if self.naalu_token else None,
            "nekro_assimilator_tokens": [token.save() for token in self.nekro_assimilator_tokens] if self.nekro_assimilator_tokens else None,
            "creuss_wormhole_tokens": [token.save() for token in self.creuss_wormhole_tokens] if self.creuss_wormhole_tokens else None,
        }

    def init_from_save(self, data: dict):
        super().init_from_save(data)

        self.players =                      MappingProxyType({id: PlayerState.load(player_data) for id, player_data in data["players"].items()})
        self.systems =                      MappingProxyType({id: SystemState.load(system_data) for id, system_data in data["systems"].items()})
        self.planets =                      MappingProxyType({id: PlanetState.load(planet_data) for id, planet_data in data["planets"].items()})
        self.speaker_token =                SpeakerTokenState.load(data["speaker_token"])
        self.custodians_token =             CustodiansTokenState.load(data["custodians_token"])
        self.deployed_units =               {id: UnitState.load(unit_data) for id, unit_data in data["deployed_units"].items()}
        self.strategy_cards =               MappingProxyType({id: StrategyCardState.load(card_data) for id, card_data in data["strategy_cards"].items()})
        self.promissory_notes =             MappingProxyType({id: PromissoryNoteCardState.load(card_data) for id, card_data in data["promissory_notes"].items()})
        self.revealed_public_objectives =   {id: PublicObjectiveCardState.load(card_data) for id, card_data in data["revealed_public_objectives"].items()}
        self.agenda_cards =                 MappingProxyType({id: AgendaCardState.load(card_data) for id, card_data in data["agenda_cards"].items()})
        self.tech_cards =                   MappingProxyType({id: TechCardState.load(card_data) for id, card_data in data["tech_cards"].items()})
        self.public_objective_i_deck =      CardDeckState[PublicObjectiveCardState].load(data["public_objective_i_deck"])
        self.public_objective_ii_deck =     CardDeckState[PublicObjectiveCardState].load(data["public_objective_ii_deck"])
        self.secret_objective_deck =        CardDeckState[SecretObjectiveCardState].load(data["secret_objective_deck"])
        self.action_card_deck =             CardDeckState[ActionCardState].load(data["action_card_deck"])
        self.naalu_token =                  NaaluTokenState.load(data["naalu_token"]) if data["naalu_token"] else None
        self.nekro_assimilator_tokens =     tuple(NekroAssimilatorTokenState.load(token) for token in data["nekro_assimilator_tokens"]) if data["nekro_assimilator_tokens"] else None
        self.creuss_wormhole_tokens =       tuple(CreussWormholeTokenState.load(token) for token in data["creuss_wormhole_tokens"]) if data["creuss_wormhole_tokens"] else None
