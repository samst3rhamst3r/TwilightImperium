"""Mirrors src/app/config/yaml_loader.py.

yaml_loader is deliberately dumb now - just file reading plus the root
subdirectory names. Per-type parsing lives next to each Config class
(``objs/<type>/loader.py``, ``setup/loader.py``) and is tested alongside it
in the mirrored ``test_objs/test_<type>/test_loader.py`` modules.
"""
from pathlib import Path

from app.config import yaml_loader

def test_path_constants_point_at_real_data_subdirectories(data_dir: Path) -> None:
    assert (data_dir / yaml_loader.CONFIG_OBJ_DATA_PATH).is_dir()
    assert (data_dir / yaml_loader.SETUP_CONFIG_DATA_PATH).is_dir()

def test_load_data_returns_parsed_yaml(tmp_path: Path) -> None:
    path = tmp_path / "sample.yaml"
    path.write_text("- id: a\n  n: 1\n- id: b\n", encoding="utf-8")
    assert yaml_loader.load_data(path) == [{"id": "a", "n": 1}, {"id": "b"}]

def test_load_data_uses_safe_load(tmp_path: Path) -> None:
    """Arbitrary-object YAML tags must be rejected, not instantiated."""
    import yaml
    import pytest

    path = tmp_path / "unsafe.yaml"
    path.write_text("!!python/object/apply:os.getcwd []\n", encoding="utf-8")
    with pytest.raises(yaml.constructor.ConstructorError):
        yaml_loader.load_data(path)

def test_load_data_reads_real_non_ascii_text(data_dir: Path) -> None:
    """Real text data contains curly apostrophes (e.g. the Devotion faction
    ability) - load_data must decode them intact regardless of platform
    default encoding."""
    entries = yaml_loader.load_data(data_dir / "text_objs" / "abilities" / "faction.yaml")
    devotion = next(e for e in entries if e["id"] == "devotion")
    assert "’" in devotion["functional_text"]  # RIGHT SINGLE QUOTATION MARK
    assert "â€" not in devotion["functional_text"]  # its UTF-8 bytes mis-decoded as cp1252
