# Quickstart: Validating Single-Unit Movement

This is the end-to-end check for this feature — SC-003 requires it be
exercisable by an automated test with no turn-sequencing/tactical-action/
fleet-management dependency. Everything below should be expressible in
`tests/test_services/test_movement.py`.

## Prerequisites

- Repo root, `.venv` active (or `pytest` on `PATH` with `pythonpath = "src"`
  from `pyproject.toml` already in effect).
- No new dependencies to install.

## Setup (what the test fixtures build)

A minimal `GameState` — no full new-game bootstrap needed:

1. Two `PlayerState`s (e.g. `red`, `blue`).
2. Two `SystemState`s whose `map_hex_coordinate`s are direct hex neighbors
   (e.g. `HexCoordinate(0, 0)` and one of its `.neighbors`), plus a third
   `SystemState` that is **not** a neighbor of either, for Story 3 / the
   non-adjacent edge case.
3. One `UnitState` located in the first system
   (`UnitLocation(loc_type=SYSTEM, location_id=<system A id>)`), owned by
   `red` via `unit.assign_owner("red")`.
4. A `RulesetConfig` (real `data/` tree via the session-scoped fixture
   pattern already used in `tests/test_config/conftest.py`) so
   `resolved_unit`/`resolved_system` can resolve real `config_id`s.
5. `GameStateResolver(game_state, ruleset_config)` → `MovementService(resolver)`.

See `data-model.md` and `contracts/movement_service.md` for the exact
shapes/signatures involved.

## Run

```powershell
pytest tests/test_services/test_movement.py -v
```

Then the full gate:

```powershell
pytest
```

## Expected outcomes (maps directly to spec Acceptance Scenarios / Edge Cases)

| Scenario | Call | Expected |
|---|---|---|
| US1 Scenario 1 | `move_unit(unit_id=U, destination_system_id=B, requesting_player_id="red")` where B is adjacent to A | Returns `None`; `deployed_units[U].location.location_id == B`; every other field of `game_state` unchanged (compare `game_state.save()` before/after, or spot-check untouched players/other systems). |
| US1 Scenario 2 | Same call | `game_state.units_in_system(A) == ()`; `game_state.units_in_system(B) == (that unit,)`. |
| US2 Scenario 1 | Same call but `requesting_player_id="blue"` | Raises `UnitOwnershipError`; unit still in A. |
| US3 Scenario 1 | `destination_system_id=C` (not adjacent) | Raises `IllegalDestinationError`; unit still in A. |
| Edge: unknown destination | `destination_system_id="does-not-exist"` | Raises `UnknownSystemError`; unit still in A. |
| Edge: unknown unit | `unit_id="does-not-exist"` | Raises `UnknownUnitError`. |
| Edge: self-move | `destination_system_id=A` | Raises `SelfMoveError`; unit still in A. |
| Edge: multi-hop chain | `destination_system_id=` a system 2+ hex rings away, reachable only via an intermediate adjacent system | Raises `IllegalDestinationError` — same as any other non-adjacent system; no multi-hop traversal is attempted. |

## Done when

- [ ] Every row above is a passing test.
- [ ] `pytest` (bare, from repo root) passes cleanly, including
      `tests/test_config` and `tests/test_state` (constitution Principle V
      gate) plus the new `tests/test_resolved` and `tests/test_services`.
- [ ] A failed move (any exception row above) leaves `game_state` bit-for-bit
      unchanged except nothing — verified by an explicit before/after
      comparison in at least one rejection test, not asserted only by
      omission.
