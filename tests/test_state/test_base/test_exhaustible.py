"""Tests for app.state.base.exhaustible.Exhaustible.

`exhausted` is a plain bool (not Optional) - whether a class can be
exhausted at all is encoded by composing this mixin, not by a None escape
hatch (ARCHITECTURE.md section 2's trait-split principle, applied to State).
"""
import pytest

from app.state.base.exhaustible import (
    Exhaustible,
    ExhaustibleAlreadyExhausted,
    ExhaustibleAlreadyReadied,
)

def test_exhaustible_defaults_to_not_exhausted() -> None:
    assert Exhaustible().exhausted is False

def test_exhaustible_exhaust_sets_exhausted_true() -> None:
    obj = Exhaustible()
    obj.exhaust()
    assert obj.exhausted is True

def test_exhaustible_exhaust_when_already_exhausted_raises() -> None:
    obj = Exhaustible(exhausted=True)
    with pytest.raises(ExhaustibleAlreadyExhausted):
        obj.exhaust()

def test_exhaustible_ready_sets_exhausted_false() -> None:
    obj = Exhaustible(exhausted=True)
    obj.ready()
    assert obj.exhausted is False

def test_exhaustible_ready_when_already_readied_raises() -> None:
    obj = Exhaustible()
    with pytest.raises(ExhaustibleAlreadyReadied):
        obj.ready()

def test_exhaustible_save_load_round_trip() -> None:
    obj = Exhaustible(exhausted=True)
    reloaded = Exhaustible.load(obj.save())
    assert reloaded.exhausted is True
