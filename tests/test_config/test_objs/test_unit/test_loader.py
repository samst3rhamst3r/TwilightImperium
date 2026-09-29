"""Mirrors src/app/config/objs/unit/loader.py."""
from types import MappingProxyType

from app.config.objs.unit import UnitConfig, load_unit_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    index = load_unit_data(data_dir)
    assert isinstance(index, MappingProxyType)
    assert index
    for key, config in index.items():
        assert isinstance(config, UnitConfig)
        assert key == config.id

def test_unit_text_is_optional_but_still_merged_when_present(data_dir) -> None:
    units = load_unit_data(data_dir).values()
    assert any(unit.functional_text is None for unit in units), (
        "expected at least one unit with no functional_text (e.g. a basic Cruiser) - "
        "if this fails, the text_required=False path may no longer be exercised by real data"
    )
    assert any(unit.functional_text for unit in units), (
        "expected at least one unit with functional_text actually merged in"
    )
