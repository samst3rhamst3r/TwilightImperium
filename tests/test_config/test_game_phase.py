"""Mirrors src/app/config/game_phase.py."""
from app.config.game_phase import GamePhase
from app.config.shared.enum import ConfigEnum

def test_game_phase_is_a_configenum() -> None:
    """GamePhase values are parsed straight out of objectives.yaml's
    game_phase field, so it needs ConfigEnum's YAML-case-strictness."""
    assert issubclass(GamePhase, ConfigEnum)

def test_game_phase_has_the_four_expected_phases() -> None:
    assert {member.value for member in GamePhase} == {"strategy", "action", "status", "agenda"}
