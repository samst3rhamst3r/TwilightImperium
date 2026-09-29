"""Mirrors src/app/config/fromdict.py."""
from dataclasses import dataclass

import pytest

from app.config.fromdict import FromDictMixin

@dataclass(frozen=True, kw_only=True)
class _Inner(FromDictMixin):
    values: tuple[int, ...]

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["values"] = tuple(d["values"])

@dataclass(frozen=True, kw_only=True)
class _Outer(FromDictMixin):
    inner: _Inner

    @classmethod
    def _init_from_dict(cls, d: dict) -> None:
        d["inner"] = _Inner.from_dict(d["inner"])

def test_from_dict_runs_init_from_dict_before_construction() -> None:
    obj = _Inner.from_dict({"values": [1, 2]})
    assert obj.values == (1, 2)

def test_from_dict_composes_through_nested_from_dict_calls() -> None:
    obj = _Outer.from_dict({"inner": {"values": [1]}})
    assert obj.inner == _Inner(values=(1,))

def test_from_dict_does_not_mutate_the_callers_dict() -> None:
    raw = {"values": [1, 2]}
    _Inner.from_dict(raw)
    assert raw == {"values": [1, 2]}

def test_from_dict_tolerates_the_same_nested_dict_shared_by_several_entries() -> None:
    """Regression: YAML anchors/aliases (e.g. ``*combat_args`` in
    data/objs/abilities/parameterized.yaml) make safe_load return the *same*
    dict object for every alias. If from_dict mutated in place, the second
    entry would receive already-converted values and fail."""
    shared = {"values": [1, 2]}
    first = _Outer.from_dict({"inner": shared})
    second = _Outer.from_dict({"inner": shared})
    assert first == second
    assert shared == {"values": [1, 2]}

def test_subclass_without_init_from_dict_raises_not_implemented() -> None:
    @dataclass(frozen=True, kw_only=True)
    class _NoHook(FromDictMixin):
        x: int

    with pytest.raises(NotImplementedError):
        _NoHook.from_dict({"x": 1})
