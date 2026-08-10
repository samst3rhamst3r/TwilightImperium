"""Mirrors src/app/config/player_color.py."""
from app.config.player_color import PlayerColor
from app.config.shared.enum import ConfigEnum, SerializableEnum

def test_player_color_is_a_serializable_enum_but_not_a_configenum() -> None:
    """PlayerColor is assigned by app/setup logic, never parsed out of a raw
    YAML value, so it deliberately doesn't need ConfigEnum's
    YAML-case-strictness - plain SerializableEnum is enough. See
    test_config_invariants.test_yaml_sourced_enums_are_configenum_subclasses
    for the enums that DO need ConfigEnum."""
    assert issubclass(PlayerColor, SerializableEnum)
    assert not issubclass(PlayerColor, ConfigEnum)

def test_player_color_has_the_six_expected_colors() -> None:
    assert {member.value for member in PlayerColor} == {
        "black", "blue", "green", "red", "purple", "yellow",
    }
