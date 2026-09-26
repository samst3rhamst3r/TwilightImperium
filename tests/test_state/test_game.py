"""Tests for app.state.game.GameState - the per-game aggregate root."""
from types import MappingProxyType

import pytest

from app.config.objs.system import WormholeType
from app.config.objs.unit import UnitLocationType
from app.config.enum.player_color import PlayerColor
from app.geometry import HexCoordinate
from app.state.card.action import ActionCardState
from app.state.card.agenda import AgendaCardState
from app.state.card.deck import CardDeckState
from app.state.card.objective.public import PublicObjectiveCardState
from app.state.card.objective.secret import SecretObjectiveCardState
from app.state.card.tech import TechCardState
from app.state.game import GameState
from app.state.planet import PlanetState
from app.state.player import PlayerState
from app.state.special_tokens import (
    CreussWormholeTokenState,
    CustodiansTokenState,
    NaaluTokenState,
    NekroAssimilatorTokenState,
    SpeakerTokenState,
)
from app.state.system import SystemState
from app.state.unit.location import UnitLocation
from app.state.unit.unit import UnitState

@pytest.fixture
def game_state_factory():
    def _make(**overrides) -> GameState:
        defaults = dict(
            players=MappingProxyType({}),
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
            public_objective_i_deck=CardDeckState(deck=[]),
            public_objective_ii_deck=CardDeckState(deck=[]),
            secret_objective_deck=CardDeckState(deck=[]),
            action_card_deck=CardDeckState(deck=[]),
            agenda_card_deck=CardDeckState(deck=[]),
            tech_card_deck=CardDeckState(deck=[]),
        )
        return GameState(**(defaults | overrides))
    return _make

def test_game_state_constructs_with_no_special_tokens_by_default(game_state_factory) -> None:
    """Regression: naalu_token/nekro_assimilator_tokens/creuss_wormhole_tokens
    used to be field(init=False) with no default, so plain construction
    raised AttributeError even when no faction needed them."""
    game = game_state_factory()
    assert game.naalu_token is None
    assert game.nekro_assimilator_tokens is None
    assert game.creuss_wormhole_tokens is None

def test_game_state_save_load_round_trip_with_no_special_tokens(game_state_factory, declared_immutable_field_violations) -> None:
    game = game_state_factory(
        players=MappingProxyType({"red": PlayerState(color=PlayerColor.RED, name="Sam", faction_config_id="sol")}),
        systems=MappingProxyType({"sys_18": SystemState(config_id="sys_18", map_hex_coordinate=HexCoordinate(0, 0))}),
        planets=MappingProxyType({"mecatol_rex": PlanetState(config_id="mecatol_rex")}),
        agenda_cards=MappingProxyType({"holy_planet_of_ixth": AgendaCardState(config_id="holy_planet_of_ixth")}),
        tech_cards=MappingProxyType({"graviton_laser_system": TechCardState(config_id="graviton_laser_system")}),
    )

    reloaded = GameState.load(game.save())

    assert set(reloaded.players) == {"red"}
    assert reloaded.players["red"].name == "Sam"
    assert set(reloaded.systems) == {"sys_18"}
    assert set(reloaded.planets) == {"mecatol_rex"}
    assert set(reloaded.agenda_cards) == {"holy_planet_of_ixth"}
    assert set(reloaded.tech_cards) == {"graviton_laser_system"}
    assert reloaded.naalu_token is None
    assert reloaded.nekro_assimilator_tokens is None
    assert reloaded.creuss_wormhole_tokens is None
    assert not declared_immutable_field_violations(reloaded)

def test_game_state_save_load_round_trip_with_all_special_tokens_present(game_state_factory, declared_immutable_field_violations) -> None:
    game = game_state_factory(
        naalu_token=NaaluTokenState(),
        nekro_assimilator_tokens=(
            NekroAssimilatorTokenState(config_id="valefar_assimilator_x"),
            NekroAssimilatorTokenState(config_id="valefar_assimilator_y"),
        ),
        creuss_wormhole_tokens=(
            CreussWormholeTokenState(wormhole_type=WormholeType.ALPHA),
            CreussWormholeTokenState(wormhole_type=WormholeType.BETA),
        ),
    )
    game.naalu_token.ownable.set_owner("red")

    reloaded = GameState.load(game.save())

    assert reloaded.naalu_token.ownable.is_owned_by_player("red")
    assert [t.config_id for t in reloaded.nekro_assimilator_tokens] == [
        "valefar_assimilator_x",
        "valefar_assimilator_y",
    ]
    assert [t.wormhole_type for t in reloaded.creuss_wormhole_tokens] == [
        WormholeType.ALPHA,
        WormholeType.BETA,
    ]
    assert not declared_immutable_field_violations(reloaded)

def test_game_state_deployed_units_and_decks_round_trip(game_state_factory) -> None:
    unit = UnitState(
        config_id="infantry",
        location=UnitLocation(loc_type=UnitLocationType.PLANET, location_id="mecatol_rex"),
    )
    game = game_state_factory(
        deployed_units={unit.instance_id: unit},
        action_card_deck=CardDeckState(deck=[ActionCardState(config_id="direct_hit", flavor_text_index=0)]),
        public_objective_i_deck=CardDeckState(deck=[PublicObjectiveCardState(config_id="mecatol_rex")]),
        secret_objective_deck=CardDeckState(deck=[SecretObjectiveCardState(config_id="destroy_their_greatest_ship")]),
    )

    reloaded = GameState.load(game.save())

    assert reloaded.deployed_units[unit.instance_id].config_id == "infantry"
    assert reloaded.action_card_deck.deck[0].config_id == "direct_hit"
    assert reloaded.public_objective_i_deck.deck[0].config_id == "mecatol_rex"
    assert reloaded.secret_objective_deck.deck[0].config_id == "destroy_their_greatest_ship"

def test_units_in_system_is_empty_for_a_system_with_no_units(game_state_factory) -> None:
    game = game_state_factory()
    assert game.units_in_system("sys_18") == ()

def test_units_in_system_returns_exactly_the_units_located_there(game_state_factory) -> None:
    in_system = UnitState(
        config_id="infantry",
        location=UnitLocation(loc_type=UnitLocationType.SYSTEM, location_id="sys_18"),
    )
    elsewhere = UnitState(
        config_id="infantry",
        location=UnitLocation(loc_type=UnitLocationType.SYSTEM, location_id="sys_25"),
    )
    game = game_state_factory(deployed_units={
        in_system.instance_id: in_system,
        elsewhere.instance_id: elsewhere,
    })

    assert game.units_in_system("sys_18") == (in_system,)

def test_units_in_system_ignores_units_on_a_planet_or_ship_with_a_matching_location_id(game_state_factory) -> None:
    """A location_id coincidentally equal to a system_id (e.g. a planet or
    ship instance sharing the same string) must not be mistaken for
    occupying that system - loc_type must also match."""
    on_planet = UnitState(
        config_id="infantry",
        location=UnitLocation(loc_type=UnitLocationType.PLANET, location_id="sys_18"),
    )
    on_ship = UnitState(
        config_id="infantry",
        location=UnitLocation(loc_type=UnitLocationType.SHIP, location_id="sys_18"),
    )
    game = game_state_factory(deployed_units={
        on_planet.instance_id: on_planet,
        on_ship.instance_id: on_ship,
    })

    assert game.units_in_system("sys_18") == ()
