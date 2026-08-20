from collections.abc import Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Self

from app.geometry.coordinate import HexCoordinate

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
    agenda_card_deck: CardDeckState[AgendaCardState]
    tech_card_deck: CardDeckState[TechCardState]

    # Special tokens - only present when the relevant faction (Naalu/Nekro/Creuss)
    # is in play this game.
    naalu_token: NaaluTokenState | None = None
    nekro_assimilator_tokens: tuple[NekroAssimilatorTokenState, NekroAssimilatorTokenState] | None = None
    creuss_wormhole_tokens: tuple[CreussWormholeTokenState, CreussWormholeTokenState] | None = None

    _hex_coordinate_index: MappingProxyType[HexCoordinate, str] = field(init=False, repr=False)

    def __post_init__(self):
        self._hex_coordinate_index = MappingProxyType({
            s.map_hex_coordinate: s.id for s in self.systems.values()
        })

    def system_at(self, hex_coordinate: HexCoordinate) -> SystemState | None:
        """Return the system at the given hex coordinate, or None if there is no system there."""
        system_id = self._hex_coordinate_index.get(hex_coordinate)
        if system_id is None:
            return None
        return self.systems[system_id]

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
            "agenda_card_deck": self.agenda_card_deck.save(),
            "tech_card_deck": self.tech_card_deck.save(),
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
        self.agenda_card_deck =             CardDeckState[AgendaCardState].load(data["agenda_card_deck"])
        self.tech_card_deck =               CardDeckState[TechCardState].load(data["tech_card_deck"])
        self.naalu_token =                  NaaluTokenState.load(data["naalu_token"]) if data["naalu_token"] else None
        self.nekro_assimilator_tokens =     tuple(NekroAssimilatorTokenState.load(token) for token in data["nekro_assimilator_tokens"]) if data["nekro_assimilator_tokens"] else None
        self.creuss_wormhole_tokens =       tuple(CreussWormholeTokenState.load(token) for token in data["creuss_wormhole_tokens"]) if data["creuss_wormhole_tokens"] else None

        # __post_init__ isn't part of the load() cooperative chain (see
        # ARCHITECTURE.md section 3's __post_init__ caveat) - recompute
        # explicitly so system_at() works on a loaded GameState too.
        self._hex_coordinate_index = MappingProxyType({
            s.map_hex_coordinate: s.id for s in self.systems.values()
        })

    @classmethod
    def new_game(
        cls,
        players: Sequence[PlayerState],
        systems: Sequence[SystemState],
        planets: Sequence[PlanetState],
    ) -> Self:
        """Create a new game state with the given players and default values for all other attributes."""
        return cls(
            players=MappingProxyType({player.id: player for player in players}),
            systems=MappingProxyType({}),
            planets=MappingProxyType({}),
            speaker_token=SpeakerTokenState(),
            custodians_token=CustodiansTokenState(),
            deployed_units={},
            strategy_cards=MappingProxyType({}),
            promissory_notes=MappingProxyType({}),
            revealed_public_objectives={},
            agenda_cards=MappingProxyType({}),
            tech_cards=MappingProxyType({}),
            public_objective_i_deck=CardDeckState[PublicObjectiveCardState](),
            public_objective_ii_deck=CardDeckState[PublicObjectiveCardState](),
            secret_objective_deck=CardDeckState[SecretObjectiveCardState](),
            action_card_deck=CardDeckState[ActionCardState](),
            agenda_card_deck=CardDeckState[AgendaCardState](),
            tech_card_deck=CardDeckState[TechCardState](),
        )