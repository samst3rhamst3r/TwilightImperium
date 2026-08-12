"""Tests for app.state.base.ownable - _PlayerOwnable, PlayerOwnableMixin, and
the convenience Protocol that forwards generic "owner" vocabulary."""
from dataclasses import dataclass

import pytest

from app.state.base.ownable import (
    AlreadyOwnedResourceException,
    NotYetOwnedResourceException,
    PlayerOwnableMixin,
    PlayerOwnableWithConvenienceProtocol,
    _PlayerOwnable,
)

def test_player_ownable_starts_unowned() -> None:
    ownable = _PlayerOwnable()
    assert not ownable.is_owned
    assert ownable.owned_by_player_id is None

def test_player_ownable_assign_owner() -> None:
    ownable = _PlayerOwnable()
    ownable.assign_owner("red")
    assert ownable.is_owned
    assert ownable.owned_by_player_id == "red"
    assert ownable.is_owned_by_player("red")
    assert not ownable.is_owned_by_player("blue")

def test_player_ownable_assign_owner_when_already_owned_raises() -> None:
    ownable = _PlayerOwnable(owned_by_player_id="red")
    with pytest.raises(AlreadyOwnedResourceException):
        ownable.assign_owner("blue")

def test_player_ownable_release_owner_when_not_owned_raises() -> None:
    ownable = _PlayerOwnable()
    with pytest.raises(NotYetOwnedResourceException):
        ownable.release_owner()

def test_player_ownable_release_owner_returns_previous_owner() -> None:
    ownable = _PlayerOwnable(owned_by_player_id="red")
    released = ownable.release_owner()
    assert released == "red"
    assert not ownable.is_owned

def test_player_ownable_reassign_owner_when_not_owned_raises() -> None:
    ownable = _PlayerOwnable()
    with pytest.raises(NotYetOwnedResourceException):
        ownable.reassign_owner("blue")

def test_player_ownable_reassign_owner_swaps_and_returns_previous_owner() -> None:
    ownable = _PlayerOwnable(owned_by_player_id="red")
    released = ownable.reassign_owner("blue")
    assert released == "red"
    assert ownable.owned_by_player_id == "blue"

def test_player_ownable_save_load_round_trip() -> None:
    ownable = _PlayerOwnable(owned_by_player_id="red")
    reloaded = _PlayerOwnable.load(ownable.save())
    assert reloaded.owned_by_player_id == "red"

@dataclass(kw_only=True)
class _DummyOwnableLeaf(PlayerOwnableMixin):
    """A leaf using bespoke vocabulary (like PlanetState's assign_control)
    instead of the generic convenience Protocol."""
    def take_control(self, player_id: str) -> None:
        self.ownable.assign_owner(player_id)

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

@dataclass(kw_only=True)
class _DummyConvenienceLeaf(PlayerOwnableWithConvenienceProtocol):
    pass

def test_player_ownable_with_convenience_protocol_forwards_generic_vocabulary() -> None:
    leaf = _DummyConvenienceLeaf()
    leaf.assign_owner("red")
    assert leaf.is_owned
    assert leaf.is_owned_by_player("red")
    released = leaf.reassign_owner("blue")
    assert released == "red"
    assert leaf.release_owner() == "blue"
    assert not leaf.is_owned
