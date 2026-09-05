"""Tests for app.services.movement.MovementService.

Each test builds on the ``movable_game`` fixture (tests/test_services/conftest.py):
a unit in system A, owned by "red", with B a direct hex neighbor of A and C
not adjacent to either.
"""
from typing import Any

import pytest

from app.services.movement import (
    IllegalDestinationError,
    SelfMoveError,
    UnitOwnershipError,
    UnknownSystemError,
    UnknownUnitError,
)

def _diff_paths(before: Any, after: Any, path: str = "") -> list[str]:
    """Returns the list of dotted/keyed paths whose value differs between
    two save() snapshots - used to prove a rejected/accepted move changed
    exactly what it should and nothing else (FR-007/SC-002)."""
    if isinstance(before, dict) and isinstance(after, dict):
        diffs: list[str] = []
        for key in before.keys() | after.keys():
            diffs.extend(_diff_paths(before.get(key), after.get(key), f"{path}.{key}" if path else str(key)))
        return diffs
    if before == after:
        return []
    return [path]

# --- User Story 1: Move a unit to an adjacent system -----------------------

def test_move_to_adjacent_system_succeeds_and_changes_nothing_else(movable_game) -> None:
    """Acceptance Scenario 1."""
    before = movable_game.game_state.save()

    movable_game.movement.move_unit(
        unit_id=movable_game.unit_id,
        destination_system_id=movable_game.system_b_id,
        requesting_player_id=movable_game.owner_player_id,
    )

    after = movable_game.game_state.save()
    diffs = _diff_paths(before, after)

    assert diffs == [f"deployed_units.{movable_game.unit_id}.location.location_id"]
    assert movable_game.game_state.deployed_units[movable_game.unit_id].location.location_id == movable_game.system_b_id

def test_move_updates_units_in_system(movable_game) -> None:
    """Acceptance Scenario 2."""
    movable_game.movement.move_unit(
        unit_id=movable_game.unit_id,
        destination_system_id=movable_game.system_b_id,
        requesting_player_id=movable_game.owner_player_id,
    )

    moved_unit = movable_game.game_state.deployed_units[movable_game.unit_id]
    assert movable_game.game_state.units_in_system(movable_game.system_a_id) == ()
    assert movable_game.game_state.units_in_system(movable_game.system_b_id) == (moved_unit,)

def test_move_unknown_unit_raises_unknown_unit_error(movable_game) -> None:
    with pytest.raises(UnknownUnitError):
        movable_game.movement.move_unit(
            unit_id="does-not-exist",
            destination_system_id=movable_game.system_b_id,
            requesting_player_id=movable_game.owner_player_id,
        )

def test_move_unknown_destination_raises_unknown_system_error(movable_game) -> None:
    with pytest.raises(UnknownSystemError):
        movable_game.movement.move_unit(
            unit_id=movable_game.unit_id,
            destination_system_id="does-not-exist",
            requesting_player_id=movable_game.owner_player_id,
        )

# --- User Story 2: Reject moving a unit you don't own -----------------------

def test_move_by_non_owner_raises_unit_ownership_error_and_changes_nothing(movable_game) -> None:
    """Acceptance Scenario 1."""
    before = movable_game.game_state.save()

    with pytest.raises(UnitOwnershipError):
        movable_game.movement.move_unit(
            unit_id=movable_game.unit_id,
            destination_system_id=movable_game.system_b_id,
            requesting_player_id=movable_game.other_player_id,
        )

    after = movable_game.game_state.save()
    assert _diff_paths(before, after) == []
    assert movable_game.game_state.deployed_units[movable_game.unit_id].location.location_id == movable_game.system_a_id

# --- User Story 3: Move only within the current legal-destination set ------

def test_move_to_non_adjacent_system_raises_illegal_destination_error_and_changes_nothing(movable_game) -> None:
    """Acceptance Scenario 1."""
    before = movable_game.game_state.save()

    with pytest.raises(IllegalDestinationError):
        movable_game.movement.move_unit(
            unit_id=movable_game.unit_id,
            destination_system_id=movable_game.system_c_id,
            requesting_player_id=movable_game.owner_player_id,
        )

    after = movable_game.game_state.save()
    assert _diff_paths(before, after) == []

def test_self_move_raises_self_move_error(movable_game) -> None:
    with pytest.raises(SelfMoveError):
        movable_game.movement.move_unit(
            unit_id=movable_game.unit_id,
            destination_system_id=movable_game.system_a_id,
            requesting_player_id=movable_game.owner_player_id,
        )

def test_multi_hop_chain_is_not_a_legal_one_move_path(movable_game) -> None:
    """System C is reachable from A only via the chain A->B->C (each hop
    individually adjacent); a single move straight to C is still illegal -
    no transitive/multi-hop traversal is attempted in one move."""
    with pytest.raises(IllegalDestinationError):
        movable_game.movement.move_unit(
            unit_id=movable_game.unit_id,
            destination_system_id=movable_game.system_c_id,
            requesting_player_id=movable_game.owner_player_id,
        )
    assert movable_game.game_state.deployed_units[movable_game.unit_id].location.location_id == movable_game.system_a_id
