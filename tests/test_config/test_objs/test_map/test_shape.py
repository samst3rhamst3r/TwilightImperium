"""Mirrors src/app/config/objs/map/shape.py."""
from app.config.objs.map import MapShape
from app.config.shared.enum import ConfigEnum

def test_map_shape_is_a_configenum() -> None:
    assert issubclass(MapShape, ConfigEnum)

def test_map_shape_has_the_two_expected_shapes() -> None:
    assert {member.value for member in MapShape} == {"standard", "triangular"}
