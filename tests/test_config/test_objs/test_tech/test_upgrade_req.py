"""Mirrors src/app/config/objs/tech/upgrade_req.py."""
from app.config.objs.tech import TechType, TechUpgradeReqConfig

def test_construction() -> None:
    req = TechUpgradeReqConfig(tech_type=TechType.PROPULSION, num=2)
    assert req.tech_type is TechType.PROPULSION
    assert req.num == 2
