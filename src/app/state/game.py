from collections.abc import Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Final, Self

from app.config.ruleset_config import RulesetConfig
from app.config.objs.system.wormhole import WormholeType
from app.config.objs.tech.ids import TechID
from app.config.objs.objective import ObjectiveType
from app.config.objs.faction.ids import FactionID
from app.geometry.coordinate import HexCoordinate

from .base import Serializable

from .planet import PlanetState
from .player import PlayerState
from .system import SystemState
from .unit import UnitState
from .special_token import (
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

_STARTING_PUBLIC_OBJECTIVES: Final[int] = 2

@dataclass(frozen=True, kw_only=True)
class GameState(Serializable):
    players: MappingProxyType[str, PlayerState]
    systems: MappingProxyType[str, SystemState]
    planets: MappingProxyType[str, PlanetState]
    speaker_token: SpeakerTokenState
    custodians_token: CustodiansTokenState
    public_objectives: MappingProxyType[str, PublicObjectiveCardState]
    secret_objectives: MappingProxyType[str, SecretObjectiveCardState]
    strategy_cards: MappingProxyType[str, StrategyCardState]
    promissory_notes: MappingProxyType[str, PromissoryNoteCardState]
    agenda_cards: MappingProxyType[str, AgendaCardState]
    action_cards: MappingProxyType[str, ActionCardState]
    tech_cards: MappingProxyType[str, TechCardState]
    # Mutable dictionary used because units are created and destroyed actively throughout the game.
    deployed_units: dict[str, UnitState] = field(default_factory=dict)
    # Special tokens - only present when the relevant faction (Naalu/Nekro/Creuss)
    # is in play this game.
    naalu_token: NaaluTokenState | None = None
    nekro_assimilator_tokens: tuple[NekroAssimilatorTokenState, NekroAssimilatorTokenState] | None = None
    creuss_wormhole_tokens: tuple[CreussWormholeTokenState, CreussWormholeTokenState] | None = None

    revealed_public_objectives: set[str] = field(default_factory=set)

    # Card decks
    public_objective_i_deck: CardDeckState
    public_objective_ii_deck: CardDeckState
    secret_objective_deck: CardDeckState
    action_card_deck: CardDeckState
    agenda_card_deck: CardDeckState

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
            "public_objectives": {id: card.save() for id, card in self.public_objectives.items()},
            "secret_objectives": {id: card.save() for id, card in self.secret_objectives.items()},
            "strategy_cards": {id: card.save() for id, card in self.strategy_cards.items()},
            "promissory_notes": {id: card.save() for id, card in self.promissory_notes.items()},
            "agenda_cards": {id: card.save() for id, card in self.agenda_cards.items()},
            "action_cards": {id: card.save() for id, card in self.action_cards.items()},
            "tech_cards": {id: card.save() for id, card in self.tech_cards.items()},
            "deployed_units": {id: unit.save() for id, unit in self.deployed_units.items()},
            "naalu_token": self.naalu_token.save() if self.naalu_token else None,
            "nekro_assimilator_tokens": [token.save() for token in self.nekro_assimilator_tokens] if self.nekro_assimilator_tokens else None,
            "creuss_wormhole_tokens": [token.save() for token in self.creuss_wormhole_tokens] if self.creuss_wormhole_tokens else None,
            "revealed_public_objectives": [self.revealed_public_objectives],
            "public_objective_i_deck": self.public_objective_i_deck.save(),
            "public_objective_ii_deck": self.public_objective_ii_deck.save(),
            "secret_objective_deck": self.secret_objective_deck.save(),
            "action_card_deck": self.action_card_deck.save(),
            "agenda_card_deck": self.agenda_card_deck.save(),
            "tech_card_deck": self.tech_card_deck.save(),
            "action_card_deck": self.action_card_deck.save(),
        }

    def init_from_save(self, data: dict):
        super().init_from_save(data)

        self.players =                      MappingProxyType({id: PlayerState.load(player_data) for id, player_data in data["players"].items()})
        self.systems =                      MappingProxyType({id: SystemState.load(system_data) for id, system_data in data["systems"].items()})
        self.planets =                      MappingProxyType({id: PlanetState.load(planet_data) for id, planet_data in data["planets"].items()})
        self.speaker_token =                SpeakerTokenState.load(data["speaker_token"])
        self.custodians_token =             CustodiansTokenState.load(data["custodians_token"])
        self.public_objectives =            MappingProxyType({id: PublicObjectiveCardState.load(card_data) for id, card_data in data["public_objectives"].items()})
        self.secret_objectives =            MappingProxyType({id: SecretObjectiveCardState.load(card_data) for id, card_data in data["secret_objectives"].items()})
        self.strategy_cards =               MappingProxyType({id: StrategyCardState.load(card_data) for id, card_data in data["strategy_cards"].items()})
        self.promissory_notes =             MappingProxyType({id: PromissoryNoteCardState.load(card_data) for id, card_data in data["promissory_notes"].items()})
        self.revealed_public_objectives =   {id: PublicObjectiveCardState.load(card_data) for id, card_data in data["revealed_public_objectives"].items()}
        self.agenda_cards =                 MappingProxyType({id: AgendaCardState.load(card_data) for id, card_data in data["agenda_cards"].items()})
        self.tech_cards =                   MappingProxyType({id: TechCardState.load(card_data) for id, card_data in data["tech_cards"].items()})
        self.action_cards =                 MappingProxyType({id: ActionCardState.load(card_data) for id, card_data in data["action_cards"].items()})
        self.deployed_units =               {id: UnitState.load(unit_data) for id, unit_data in data["deployed_units"].items()}
        self.naalu_token =                  NaaluTokenState.load(data["naalu_token"]) if data["naalu_token"] else None
        self.nekro_assimilator_tokens =     tuple(NekroAssimilatorTokenState.load(token) for token in data["nekro_assimilator_tokens"]) if data["nekro_assimilator_tokens"] else None
        self.creuss_wormhole_tokens =       tuple(CreussWormholeTokenState.load(token) for token in data["creuss_wormhole_tokens"]) if data["creuss_wormhole_tokens"] else None
        self.public_objective_i_deck =      CardDeckState.load(data["public_objective_i_deck"])
        self.public_objective_ii_deck =     CardDeckState.load(data["public_objective_ii_deck"])
        self.secret_objective_deck =        CardDeckState.load(data["secret_objective_deck"])
        self.action_card_deck =             CardDeckState.load(data["action_card_deck"])
        self.agenda_card_deck =             CardDeckState.load(data["agenda_card_deck"])
        self.tech_card_deck =               CardDeckState.load(data["tech_card_deck"])
        self.action_card_deck =             CardDeckState.load(data["action_card_deck"])

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
        ruleset_config: RulesetConfig
    ) -> Self:
        """Create a new game state with the given players and default values for all other attributes."""
        
        players_ = MappingProxyType({player.id: player for player in players})
        systems_ = MappingProxyType({system.id: system for system in systems})

        factions = {player.faction_config_id: player for player in players}
        
        player_home_systems = {}
        for faction_id, player in factions.items():
            faction = ruleset_config.factions[faction_id]
            player_home_systems[faction.home_system_id] = player.id
            if faction.off_board_home_system_id is not None:
                player_home_systems[faction.off_board_home_system_id] = player.id

        planets: dict[str, PlanetState] = {}
        for planet_cfg in ruleset_config.planets.values():
            if planet_cfg.system_id in systems_:
                planet = PlanetState(config_id=planet_cfg.id)
                if planet_cfg.system_id in player_home_systems:
                    planet.assign_control(player_home_systems[planet_cfg.system_id])
                planets[planet.id] = planet

        promissory_notes: dict[str, PromissoryNoteCardState] = {}
        for note_cfg in ruleset_config.promissory_notes.values():
            if note_cfg.faction_exclusive_id is None:
                for player in players:
                    promissory_note = PromissoryNoteCardState(config_id=note_cfg.id, issuing_player_color=player.color)
                    promissory_notes[promissory_note.id] = promissory_note
            elif note_cfg.faction_exclusive_id in factions:
                promissory_note = PromissoryNoteCardState(config_id=note_cfg.id)
                promissory_notes[promissory_note.id] = promissory_note
            else:
                raise ValueError(f"Promissory note {note_cfg.id} is faction-exclusive to {note_cfg.faction_exclusive_id}, which is not in play this game.")

        strategy_cards = [StrategyCardState(config_id=card.id) for card in ruleset_config.strategy_cards.values()]
        agenda_cards = [AgendaCardState(config_id=card.id) for card in ruleset_config.agendas.values()]

        action_cards: dict[str, ActionCardState] = {}
        for card_cfg in ruleset_config.action_cards.values():
            for i in range(card_cfg.num_in_deck):
                action_card = ActionCardState(config_id=card_cfg.id, flavor_text_index=i)
                action_cards[action_card.id] = action_card

        tech_cards: dict[str, TechCardState] = {}
        for faction_id, player in factions.items():
            if faction_id in factions:
                for starting_tech_id in ruleset_config.factions[faction_id].starting_tech_ids:
                    starting_tech = TechCardState(config_id=starting_tech_id)
                    player.research_tech(starting_tech.id)
                    tech_cards[starting_tech.id] = starting_tech

        pub_i: dict[str, PublicObjectiveCardState] = {}
        pub_ii: dict[str, PublicObjectiveCardState] = {}
        sec: dict[str, SecretObjectiveCardState] = {}
        for card in ruleset_config.objectives.values():
            if card.objective_type is ObjectiveType.PUBLIC_STAGE_I:
                obj = PublicObjectiveCardState(config_id=card.id)
                pub_i[obj.id] = obj
            elif card.objective_type is ObjectiveType.PUBLIC_STAGE_II:
                obj = PublicObjectiveCardState(config_id=card.id)
                pub_ii[obj.id] = obj
            elif card.objective_type is ObjectiveType.SECRET:
                obj = SecretObjectiveCardState(config_id=card.id)
                sec[obj.id] = obj

        naalu_token: NaaluTokenState | None = None
        if FactionID.NAALU_COLLECTIVE in factions:
            naalu_token = NaaluTokenState.new_game(factions[FactionID.NAALU_COLLECTIVE].id)

        nekro_assimilator_tokens: tuple[NekroAssimilatorTokenState, NekroAssimilatorTokenState] | None = None
        if FactionID.NEKRO_VIRUS in factions:
            nekro_assimilator_tokens = NekroAssimilatorTokenState.new_game()

        creuss_wormhole_tokens: tuple[CreussWormholeTokenState, CreussWormholeTokenState] | None = None
        if FactionID.GHOSTS_OF_CREUSS in factions:
            creuss_wormhole_tokens = CreussWormholeTokenState.new_game()

        obj = cls(
            players=players_,
            systems=systems_,
            planets=MappingProxyType(planets),
            speaker_token=SpeakerTokenState(),
            custodians_token=CustodiansTokenState(),
            public_objectives=MappingProxyType(pub_i | pub_ii),
            secret_objectives=MappingProxyType(sec),
            strategy_cards=MappingProxyType({card.id: card for card in strategy_cards}),
            promissory_notes=MappingProxyType(promissory_notes),
            agenda_cards=MappingProxyType({card.id: card for card in agenda_cards}),
            action_cards=MappingProxyType(action_cards),
            tech_cards=MappingProxyType(tech_cards),
            public_objective_i_deck=CardDeckState.new_game(pub_i),
            public_objective_ii_deck=CardDeckState.new_game(pub_ii),
            secret_objective_deck=CardDeckState.new_game(sec),
            action_card_deck=CardDeckState.new_game(action_cards),
            agenda_card_deck=CardDeckState.new_game([card.id for card in agenda_cards]),
            naalu_token=naalu_token,
            nekro_assimilator_tokens=nekro_assimilator_tokens,
            creuss_wormhole_tokens=creuss_wormhole_tokens,
        )

        for player in obj.players.values():
            objective_id = obj.secret_objective_deck.draw()
            objective = obj.secret_objectives[objective_id]
            objective.give_to_player(player.id)

        for i in range(_STARTING_PUBLIC_OBJECTIVES):
            objective = obj.public_objective_i_deck.draw()
            obj.revealed_public_objectives.add(objective)

        return obj