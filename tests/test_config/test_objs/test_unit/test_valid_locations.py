"""Mirrors UnitConfig.valid_locations in src/app/config/objs/unit/unit.py."""
import pytest

from app.config.objs.unit import UnitClass, UnitConfig, UnitID, UnitLocationType

def _unit(*, id: str = "x", unit_class: UnitClass) -> UnitConfig:
    return UnitConfig(id=id, name="X", unit_class=unit_class, cost=1, combat=1, move=1, capacity=0)

@pytest.mark.parametrize("unit_class", list(UnitClass), ids=[c.value for c in UnitClass])
def test_valid_locations_covers_every_unit_class(unit_class: UnitClass) -> None:
    """Every UnitClass must resolve without KeyError - the same coverage
    gap that get_unit_limit_per_player guards against (see test_limits.py),
    but for the class -> valid-locations table instead."""
    locations = _unit(unit_class=unit_class).valid_locations
    assert len(locations) > 0
    assert all(isinstance(loc, UnitLocationType) for loc in locations)

@pytest.mark.parametrize(
    "unit_id", [UnitID.FLOATING_FACTORY_I, UnitID.FLOATING_FACTORY_II], ids=lambda i: i.value
)
def test_floating_factory_ids_use_the_per_id_override_not_the_class_default(unit_id: UnitID) -> None:
    """Both Floating Factories are unit_class=SPACE_DOCK, whose class-level
    default is PLANET-only - but the two special IDs are explicitly
    overridden to SYSTEM-only in _VALID_LOCATIONS_BY_CONFIG_ID. This
    confirms the per-id override actually takes priority over the
    per-class fallback, not just that both tables independently exist."""
    unit = _unit(id=unit_id, unit_class=UnitClass.SPACE_DOCK)
    assert unit.valid_locations == (UnitLocationType.SYSTEM,)

def test_space_dock_class_default_is_planet_only_when_not_a_floating_factory() -> None:
    ordinary_space_dock = _unit(id="space_dock_i", unit_class=UnitClass.SPACE_DOCK)
    assert ordinary_space_dock.valid_locations == (UnitLocationType.PLANET,)

def test_real_unit_data_resolves_valid_locations_for_every_unit(ruleset_config) -> None:
    for unit in ruleset_config.units.values():
        locations = unit.valid_locations  # must not raise
        assert len(locations) > 0
