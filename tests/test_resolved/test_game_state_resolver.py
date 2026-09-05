"""Tests for app.resolved.game_state_resolver.GameStateResolver.resolved_system.

Only the new resolved_system(...) accessor this feature adds - the
pre-existing resolved_player/resolved_unit/resolved_planet methods have no
test coverage of their own yet (tracked in
specs/002-resolved-layer/plan.md's open Principle V item), which is not
this feature's job to close.
"""
from types import MappingProxyType

import pytest

from app.config.ruleset_config import RulesetConfig
from app.geometry import HexCoordinate
from app.resolved.game_state_resolver import GameStateResolver
from app.resolved.system import ResolvedSystem
from app.state.card.action import ActionCardState
from app.state.card.agenda import AgendaCardState
from app.state.card.deck import CardDeckState
from app.state.card.objective.public import PublicObjectiveCardState
from app.state.card.objective.secret import SecretObjectiveCardState
from app.state.card.tech import TechCardState
from app.state.game import GameState
from app.state.special_tokens import CustodiansTokenState, SpeakerTokenState
from app.state.system import SystemState

@pytest.fixture
def game_state_with_one_system() -> GameState:
    return GameState(
        players=MappingProxyType({}),
        systems=MappingProxyType({
            "01": SystemState(config_id="01", map_hex_coordinate=HexCoordinate(0, 0)),
        }),
        planets=MappingProxyType({}),
        speaker_token=SpeakerTokenState(),
        custodians_token=CustodiansTokenState(),
        deployed_units={},
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

def test_resolved_system_resolves_a_real_system(game_state_with_one_system: GameState, ruleset_config: RulesetConfig) -> None:
    resolver = GameStateResolver(game_state_with_one_system, ruleset_config)

    resolved = resolver.resolved_system("01")

    assert isinstance(resolved, ResolvedSystem)
    assert resolved.state is game_state_with_one_system.systems["01"]
    assert resolved.config.id == "01"

def test_resolved_system_raises_key_error_for_unknown_system_id(game_state_with_one_system: GameState, ruleset_config: RulesetConfig) -> None:
    resolver = GameStateResolver(game_state_with_one_system, ruleset_config)

    with pytest.raises(KeyError):
        resolver.resolved_system("does-not-exist")
