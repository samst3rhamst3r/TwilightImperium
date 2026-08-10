"""Mirrors src/app/config/objs/objective/objective.py."""
import pytest

from app.config.game_phase import GamePhase
from app.config.objs.objective import ObjectiveConfig, ObjectiveType
from app.config.shared import NamedConfigObj, RequiresFunctionalText

def test_objective_config_composes_the_expected_mixins() -> None:
    assert issubclass(ObjectiveConfig, NamedConfigObj)
    assert issubclass(ObjectiveConfig, RequiresFunctionalText)

@pytest.mark.parametrize(
    "objective_type, expected_points",
    [
        (ObjectiveType.PUBLIC_STAGE_I, 1),
        (ObjectiveType.PUBLIC_STAGE_II, 2),
        (ObjectiveType.SECRET, 1),
    ],
)
def test_victory_points_match_objective_type(objective_type: ObjectiveType, expected_points: int) -> None:
    objective = ObjectiveConfig(
        id="x", name="X", functional_text="...", objective_type=objective_type, game_phase=GamePhase.STATUS,
    )
    assert objective.victory_points == expected_points

def test_real_objective_data_has_valid_victory_points(ruleset_config) -> None:
    for objective in ruleset_config.objectives.values():
        assert objective.victory_points in (1, 2)
