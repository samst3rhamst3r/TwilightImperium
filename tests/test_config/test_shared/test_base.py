"""Mirrors src/app/config/shared/base.py."""
from dataclasses import dataclass

from app.config.shared.base import BaseConfigObj

@dataclass(frozen=True, kw_only=True)
class _Sample(BaseConfigObj):
    value: int

    @classmethod
    def _parse_fields(cls, d: dict) -> None:
        super()._parse_fields(d)
        d["value"] = int(d["value"])

def test_from_dict_runs_parse_fields_before_constructing() -> None:
    assert _Sample.from_dict({"value": "3"}) == _Sample(value=3)

def test_base_parse_fields_is_a_no_op_hook() -> None:
    d = {"value": 1}
    BaseConfigObj._parse_fields(d)
    assert d == {"value": 1}
