# Phase 1 Data Model: Single-Unit Movement

This feature adds one State-layer relationship, one Resolved-layer class,
one derived query, and one Service — no new persistent entity. Fields shown
as **NEW** are additions to existing classes; everything else is existing
shape included for context.

## `UnitState` (`src/app/state/unit/unit.py`) — MODIFIED

```python
@dataclass(kw_only=True)
class UnitState(UUIDInstancedStateObj, PlayerOwnableWithConvenienceProtocol):
    location: UnitLocation
    current_damage: int = 0
    # NEW (via PlayerOwnableWithConvenienceProtocol): ownable: _PlayerOwnable
    #   -> .assign_owner(player_id) / .is_owned_by_player(player_id) / etc.
```

- **Relationship**: a `PlayerState` owns many `UnitState`s (1:many). Per
  ARCHITECTURE.md §6 rule 1, the reference is stored on the "many" side —
  `UnitState.ownable.owned_by_player_id`, via the existing
  `PlayerOwnableWithConvenienceProtocol` mixin (no new field type
  introduced; reuses `_PlayerOwnable`).
- **Validation**: unchanged from the mixin's existing behavior —
  `assign_owner` raises `AlreadyOwnedResourceException` if called twice
  without a `release_owner`/`reassign_owner` in between. This feature does
  not call `assign_owner` from any production code path itself (no
  "assign a new unit's owner at construction" flow exists yet in this
  codebase); it's exercised directly in test fixtures, the same way
  `PlanetState.assign_control` and `StrategyCardState`'s ownership fields
  are exercised only in tests today.
- **No state transition beyond the existing one**: `location` already
  transitions via `place_in_system`/`place_on_planet`/`place_on_ship`; this
  feature calls the existing `place_in_system(system_id)` from
  `MovementService`, no new State method needed on `UnitState` itself.

## `GameState` (`src/app/state/game.py`) — MODIFIED

```python
def units_in_system(self, system_id: str) -> tuple[UnitState, ...]:
    """Derived, not stored - every unit currently located directly in the
    given system. Mirrors system_at()'s existing derive-on-demand shape."""
    return tuple(
        unit for unit in self.deployed_units.values()
        if unit.location.is_in_system and unit.location.location_id == system_id
    )
```

- Pure derived filter over the existing `deployed_units` dict + each unit's
  own `location` — no new field, no synced/cached list (ARCHITECTURE.md §6).

## `ResolvedSystem` (`src/app/resolved/system.py`) — NEW

```python
@dataclass(slots=True, frozen=True)
class ResolvedSystem(BaseResolvedObj[SystemState, SystemConfig]):
    pass
```

- Identical shape to today's `ResolvedUnit`/`ResolvedPlanet` (no methods
  beyond the generic `state`/`config` fields) — see research.md Decision 2
  for why it's built now despite no method yet reading `self.config`.

## `GameStateResolver` (`src/app/resolved/game_state_resolver.py`) — MODIFIED

```python
def resolved_system(self, system_id: str) -> ResolvedSystem:
    system_state = self._game_state.systems[system_id]
    system_config = self._ruleset_config.systems[system_state.config_id]
    return ResolvedSystem(system_state, system_config)
```

- Same shape as the three existing `resolved_*` methods — a `KeyError`
  propagates on an unknown `system_id`, caught and translated by
  `MovementService` (not by the resolver itself, consistent with how
  `resolved_unit`/`resolved_planet` behave today).

## `MovementService` (`src/app/services/movement.py`) — MODIFIED (currently an empty stub)

```python
class MovementError(Exception):
    """Base for every rejection MovementService.move_unit can raise."""

class UnknownUnitError(MovementError): ...
class UnknownSystemError(MovementError): ...
class UnitOwnershipError(MovementError): ...
class SelfMoveError(MovementError): ...
class IllegalDestinationError(MovementError): ...

class MovementService(BaseService):
    def move_unit(
        self,
        *,
        unit_id: str,
        destination_system_id: str,
        requesting_player_id: str,
    ) -> None:
        ...
```

**Preconditions** (checked in this order — see research.md Decision 4):

1. `unit_id` resolves via `self._resolver.resolved_unit(unit_id)` → else `UnknownUnitError`.
2. `destination_system_id` resolves via `self._resolver.resolved_system(...)` → else `UnknownSystemError`.
3. `resolved_unit.state.is_owned_by_player(requesting_player_id)` → else `UnitOwnershipError`.
4. `destination_system_id != resolved_unit.state.location.location_id` → else `SelfMoveError`.
5. `destination_system.state.map_hex_coordinate` is in
   `origin_system.state.map_hex_coordinate.neighbors` → else `IllegalDestinationError`.

**Postcondition on success**: `resolved_unit.state.place_in_system(destination_system_id)`
is the *only* mutation performed — no other `UnitState`, no `SystemState`,
no `PlayerState` is touched (FR-007). `SystemState` was never storing units
in the first place, so there is nothing on the System side to update.

**No new Resolved-layer method was added for the mutation itself**
(`place_in_system` is called as `resolved_unit.state.place_in_system(...)`,
not wrapped in a new `ResolvedUnit.move_to(...)` method) — per Resolved-layer
Rule 2, a `Resolved*` method only earns its place by reading `self.config`;
this move performs no Config-aware check on the unit itself (fleet
capacity, move range — explicitly out of scope), so wrapping it would be a
redundant pure forward.

## Entity summary (spec's Key Entities, mapped to concrete types)

| Spec entity | Concrete type(s) |
|---|---|
| Unit | `UnitState` (+ `UnitConfig` via `ResolvedUnit`, unused by this feature's own logic but present in the binding) |
| System | `SystemState` (+ `SystemConfig` via the new `ResolvedSystem`) |
| Player | `PlayerState.id` (a `PlayerColor` string) — only ever referenced by id (`requesting_player_id`), never resolved to a full `ResolvedPlayer` since `MovementService` needs no `FactionConfig` data |
