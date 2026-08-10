"""Mirrors src/app/config/objs/tech/upgrade_req.py."""
from app.config.objs.tech import TechType, TechUpgradeReqConfig
from app.config.shared import BaseConfigObj

def test_tech_upgrade_req_config_inherits_base_config_obj() -> None:
    assert issubclass(TechUpgradeReqConfig, BaseConfigObj)

def test_construction() -> None:
    req = TechUpgradeReqConfig(tech_type=TechType.PROPULSION, num=2)
    assert req.tech_type is TechType.PROPULSION
    assert req.num == 2
