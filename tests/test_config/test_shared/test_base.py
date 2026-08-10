"""Mirrors src/app/config/shared/base.py."""
import dataclasses

from app.config.shared.base import BaseConfigObj

def test_base_config_obj_is_a_frozen_dataclass_with_no_generated_init() -> None:
    assert dataclasses.is_dataclass(BaseConfigObj)
    params = BaseConfigObj.__dataclass_params__
    assert params.frozen
    assert not params.init  # init=False - a marker/root, never constructed directly

def test_base_config_obj_declares_no_fields_of_its_own() -> None:
    assert dataclasses.fields(BaseConfigObj) == ()
