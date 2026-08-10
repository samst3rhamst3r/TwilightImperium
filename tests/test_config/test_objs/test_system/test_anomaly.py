"""Mirrors src/app/config/objs/system/anomaly.py."""
from app.config.objs.system import AnomalyType
from app.config.shared.enum import ConfigEnum

def test_anomaly_type_is_a_configenum() -> None:
    assert issubclass(AnomalyType, ConfigEnum)

def test_anomaly_type_has_the_expected_members() -> None:
    assert {member.value for member in AnomalyType} == {
        "asteroid_field", "nebula", "supernova", "gravity_rift",
    }
