"""Shared fixtures for the ``test_services`` suite.

``data_dir``/``ruleset_config`` mirror ``tests/test_config/conftest.py`` (see
``tests/test_resolved/conftest.py`` for the identical rationale - this
package doesn't have the full discovery/sweep machinery test_config/test_state
have, scoped strictly to what this feature needs).

``movable_game`` builds the minimal two-player, three-system, one-unit
``GameState`` from quickstart.md's Setup section: system A and B are direct
hex neighbors, C is a neighbor of B but not of A (adjacent-but-one-hop-
removed, doubling as the multi-hop-chain edge case), and the one deployed
unit starts in A, owned by "red".
"""
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

import pytest

from app.config.objs.unit import UnitLocationType
from app.config.enum.player_color import PlayerColor
from app.config.ruleset_config import RulesetConfig
from app.geometry import HexCoordinate
from app.resolved.game_state_resolver import GameStateResolver
from app.services.movement import MovementService
from app.state.card.action import ActionCardState
from app.state.card.agenda import AgendaCardState
from app.state.card.deck import CardDeckState
from app.state.card.objective.public import PublicObjectiveCardState
from app.state.card.objective.secret import SecretObjectiveCardState
from app.state.card.tech import TechCardState
from app.state.game import GameState
from app.state.player import PlayerState
from app.state.special_tokens import CustodiansTokenState, SpeakerTokenState
from app.state.system import SystemState
from app.state.unit.location import UnitLocation
from app.state.unit.unit import UnitState

@pytest.fixture(scope="session")
def data_dir() -> Path:
    return Path("data")

@pytest.fixture(scope="session")
def ruleset_config(data_dir: Path) -> RulesetConfig:
    """The full ruleset, loaded once from the real data/ tree."""
    return RulesetConfig.load(data_dir)

@dataclass
class MovableGame:
    """Bundles the minimal game + wiring every MovementService test needs,
    per quickstart.md's Setup section."""
    game_state: GameState
    resolver: GameStateResolver
    movement: MovementService
    unit_id: str
    system_a_id: str
    system_b_id: str
    system_c_id: str
    owner_player_id: str
    other_player_id: str

@pytest.fixture
def movable_game(ruleset_config: RulesetConfig) -> MovableGame:
    system_a_id, system_b_id, system_c_id = "01", "02", "03"
    owner_player_id, other_player_id = "red", "blue"

    unit = UnitState(
        config_id="infantry_i",
        location=UnitLocation(loc_type=UnitLocationType.SYSTEM, location_id=system_a_id),
    )
    unit.ownable.set_owner(owner_player_id)

    game_state = GameState(
        players=MappingProxyType({
            owner_player_id: PlayerState(color=PlayerColor.RED, name="Red Player", faction_config_id="federation_of_sol"),
            other_player_id: PlayerState(color=PlayerColor.BLUE, name="Blue Player", faction_config_id="mentak_coalition"),
        }),
        systems=MappingProxyType({
            # A and B are direct hex neighbors (B = one of A's six neighbors).
            # C is a neighbor of B but NOT of A - not adjacent to A directly,
            # but reachable via the chain A->B->C, exercising both "plain
            # non-adjacent destination" and the "multi-hop chain isn't a
            # legal one-move path" edge case with the same system.
            system_a_id: SystemState(config_id=system_a_id, map_hex_coordinate=HexCoordinate(0, 0)),
            system_b_id: SystemState(config_id=system_b_id, map_hex_coordinate=HexCoordinate(1, 0)),
            system_c_id: SystemState(config_id=system_c_id, map_hex_coordinate=HexCoordinate(2, -1)),
        }),
        planets=MappingProxyType({}),
        speaker_token=SpeakerTokenState(),
        custodians_token=CustodiansTokenState(),
        deployed_units={unit.instance_id: unit},
        strategy_cards=MappingProxyType({}),
        promissory_notes=MappingProxyType({}),
        revealed_public_objectives={},
        agenda_cards=MappingProxyType({}),
        tech_cards=MappingProxyType({}),
        public_objective_i_deck=CardDeckState[PublicObjectiveCardState](deck=[]),
        public_objective_ii_deck=CardDeckState[PublicObjectiveCardState](deck=[]),
        secret_objective_deck=CardDeckState[SecretObjectiveCardState](deck=[]),
        action_card_deck=CardDeckState[ActionCardState](deck=[]),
        agenda_card_deck=CardDeckState[AgendaCardState](deck=[]),
        tech_card_deck=CardDeckState[TechCardState](deck=[]),
    )

    resolver = GameStateResolver(game_state, ruleset_config)
    movement = MovementService(resolver)

    return MovableGame(
        game_state=game_state,
        resolver=resolver,
        movement=movement,
        unit_id=unit.instance_id,
        system_a_id=system_a_id,
        system_b_id=system_b_id,
        system_c_id=system_c_id,
        owner_player_id=owner_player_id,
        other_player_id=other_player_id,
    )
