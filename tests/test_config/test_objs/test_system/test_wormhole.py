"""Mirrors src/app/config/objs/system/wormhole.py."""
from app.config.objs.system import WormholeType
from app.config.shared.enum import ConfigEnum

def test_wormhole_type_is_a_configenum() -> None:
    assert issubclass(WormholeType, ConfigEnum)

def test_wormhole_type_has_the_expected_members() -> None:
    assert {member.value for member in WormholeType} == {"alpha", "beta", "delta"}
