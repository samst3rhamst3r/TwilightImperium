"""Tests for app.state.base.ownable - _PlayerOwnable and PlayerOwnableMixin.

There is no more generic "convenience Protocol" forwarding owner vocabulary
onto a leaf class - every leaf (with or without bespoke vocabulary like
Planet's "control") reaches ownership through its own `.ownable` field
directly (`leaf.ownable.set_owner(...)`, `leaf.ownable.is_owned_by_player(...)`).
"""
from dataclasses import dataclass

import pytest

from app.state.base.ownable import (
    NotYetOwnedResourceException,
    PlayerOwnableMixin,
    _PlayerOwnable,
)

def test_player_ownable_starts_unowned() -> None:
    ownable = _PlayerOwnable()
    assert not ownable.is_owned
    assert ownable.owned_by_player_id is None

def test_player_ownable_set_owner() -> None:
    ownable = _PlayerOwnable()
    ownable.set_owner("red")
    assert ownable.is_owned
    assert ownable.owned_by_player_id == "red"
    assert ownable.is_owned_by_player("red")
    assert not ownable.is_owned_by_player("blue")

def test_player_ownable_set_owner_overwrites_an_existing_owner() -> None:
    """set_owner is unconditional - no AlreadyOwnedResourceException guard;
    a caller wanting swap-with-the-old-owner-returned semantics uses
    release_owner() + set_owner() explicitly (see PlanetState.reassign_control)."""
    ownable = _PlayerOwnable(owned_by_player_id="red")
    ownable.set_owner("blue")
    assert ownable.owned_by_player_id == "blue"

def test_player_ownable_release_owner_when_not_owned_raises() -> None:
    ownable = _PlayerOwnable()
    with pytest.raises(NotYetOwnedResourceException):
        ownable.release_owner()

def test_player_ownable_release_owner_returns_previous_owner() -> None:
    ownable = _PlayerOwnable(owned_by_player_id="red")
    released = ownable.release_owner()
    assert released == "red"
    assert not ownable.is_owned

def test_player_ownable_save_load_round_trip() -> None:
    ownable = _PlayerOwnable(owned_by_player_id="red")
    reloaded = _PlayerOwnable.load(ownable.save())
    assert reloaded.owned_by_player_id == "red"

@dataclass(kw_only=True)
class _DummyOwnableLeaf(PlayerOwnableMixin):
    """A leaf using bespoke vocabulary (like PlanetState's assign_control)."""
    def take_control(self, player_id: str) -> None:
        self.ownable.set_owner(player_id)

def test_player_ownable_mixin_composes_a_fresh_ownable_by_default() -> None:
    leaf = _DummyOwnableLeaf()
    assert not leaf.ownable.is_owned

def test_player_ownable_mixin_bespoke_vocabulary_forwards_through_ownable() -> None:
    leaf = _DummyOwnableLeaf()
    leaf.take_control("red")
    assert leaf.ownable.is_owned_by_player("red")

def test_player_ownable_mixin_save_load_round_trip() -> None:
    leaf = _DummyOwnableLeaf()
    leaf.take_control("red")
    reloaded = _DummyOwnableLeaf.load(leaf.save())
    assert reloaded.ownable.is_owned_by_player("red")
