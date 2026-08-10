"""Mirrors src/app/config/objs/system/tile_color.py."""
from app.config.objs.system import TileColor
from app.config.shared.enum import ConfigEnum

def test_tile_color_is_a_configenum() -> None:
    assert issubclass(TileColor, ConfigEnum)

def test_tile_color_has_the_expected_members() -> None:
    assert {member.value for member in TileColor} == {"red", "blue", "green"}
