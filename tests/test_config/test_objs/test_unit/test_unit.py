"""Mirrors src/app/config/objs/unit/unit.py."""
from app.config.objs.unit import UnitClass, UnitConfig
from app.config.shared import CanHaveFactionExclusivity, NamedConfigObj

def _make(**overrides):
    defaults = dict(id="x", name="X", unit_class=UnitClass.CRUISER, cost=1, combat=1, move=1, capacity=0)
    return UnitConfig(**(defaults | overrides))

def test_unit_config_composes_the_expected_mixins() -> None:
    assert issubclass(UnitConfig, NamedConfigObj)
    assert issubclass(UnitConfig, CanHaveFactionExclusivity)

def test_unit_config_does_not_require_functional_text_mixin() -> None:
    """Unlike most Config types, functional_text is an optional plain field
    here (str | None = None), not the mandatory RequiresFunctionalText
    mixin - plenty of real units (basic Cruisers, Destroyers) have no
    special ability text."""
    from app.config.shared import RequiresFunctionalText

    assert not issubclass(UnitConfig, RequiresFunctionalText)

def test_can_move_is_false_when_move_is_none_or_zero() -> None:
    assert _make(move=None).can_move is False
    assert _make(move=0).can_move is False
    assert _make(move=1).can_move is True

def test_can_carry_units_is_false_when_capacity_is_none_or_zero() -> None:
    assert _make(capacity=None).can_carry_units is False
    assert _make(capacity=0).can_carry_units is False
    assert _make(capacity=2).can_carry_units is True
