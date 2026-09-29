"""Mirrors src/app/config/objs/system/loader.py."""
from types import MappingProxyType

from app.config.objs.system import SystemConfig, load_system_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    index = load_system_data(data_dir)
    assert isinstance(index, MappingProxyType)
    assert index
    for key, config in index.items():
        assert isinstance(config, SystemConfig)
        assert key == config.id

def test_loads_without_a_text_objs_file(data_dir) -> None:
    """systems.yaml has no text_objs counterpart - the loader must read
    objs/ directly rather than requiring a text merge."""
    assert not (data_dir / "text_objs" / "systems.yaml").exists()
    assert load_system_data(data_dir)
