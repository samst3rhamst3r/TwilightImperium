"""Mirrors src/app/config/objs/unit/limits.py."""
import pytest

from app.config.objs.unit import UnitClass, get_component_limit_per_player, get_unit_limit_per_player

@pytest.mark.parametrize("unit_class", list(UnitClass), ids=[c.value for c in UnitClass])
def test_get_unit_limit_per_player_covers_every_unit_class(unit_class: UnitClass) -> None:
    """Every UnitClass must resolve without KeyError - a class added to the
    enum without a corresponding limits-table entry would otherwise only
    surface as a crash the first time that unit type is produced in a real
    game."""
    get_unit_limit_per_player(unit_class)  # must not raise

def test_fighters_and_infantry_have_no_per_player_class_limit() -> None:
    """Fighters/Infantry are only limited at the component-token level (see
    get_component_limit_per_player), not by a per-player unit count."""
    assert get_unit_limit_per_player(UnitClass.FIGHTER) is None
    assert get_unit_limit_per_player(UnitClass.INFANTRY) is None

def test_flagship_limit_is_one() -> None:
    assert get_unit_limit_per_player(UnitClass.FLAGSHIP) == 1

@pytest.mark.parametrize("unit_class", list(UnitClass), ids=[c.value for c in UnitClass])
def test_get_component_limit_per_player_covers_every_unit_class(unit_class: UnitClass) -> None:
    """Falls back to the per-player class limit table for any class without
    its own component-limit entry - must never KeyError."""
    get_component_limit_per_player(unit_class)  # must not raise

def test_component_limits_override_the_class_limit_for_fighters_and_infantry() -> None:
    assert get_component_limit_per_player(UnitClass.FIGHTER) == 10
    assert get_component_limit_per_player(UnitClass.INFANTRY) == 12
