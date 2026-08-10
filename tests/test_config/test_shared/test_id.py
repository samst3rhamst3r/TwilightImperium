"""Mirrors src/app/config/shared/id.py."""
from app.config.shared.base import BaseConfigObj
from app.config.shared.id import IDConfigObj

def test_id_config_obj_inherits_base_config_obj() -> None:
    assert issubclass(IDConfigObj, BaseConfigObj)

def test_str_returns_the_id() -> None:
    obj = IDConfigObj(id="some_id")
    assert str(obj) == "some_id"

def test_id_config_obj_is_frozen_and_kw_only() -> None:
    params = IDConfigObj.__dataclass_params__
    assert params.frozen
    assert params.kw_only
