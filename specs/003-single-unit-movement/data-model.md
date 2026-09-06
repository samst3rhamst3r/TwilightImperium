# Phase 1 Data Model: Single-Unit Movement

This feature adds one State-layer relationship, one Resolved-layer class,
one derived query, and one Service — no new persistent entity. Fields shown
as **NEW** are additions to existing classes; everything else is existing
shape included for context.

## `UnitState` (`src/app/state/unit/unit.py`) — MODIFIED

```python
class UnitOwnershipError(OwnershipError):
    """Raised when a requesting player doesn't own the unit being acted on."""
    entity_name: str = "unit"

@dataclass(kw_only=True)
class UnitState(UUIDInstancedStateObj, PlayerOwnableMixin):
    location: UnitLocation
    current_damage: int = 0
    # NEW (via PlayerOwnableMixin): ownable: _PlayerOwnable
    #   -> .ownable.set_owner(player_id) / .ownable.is_owned_by_player(player_id) / etc.
    # No forwarding methods on UnitState itself - reached via .ownable.*
    # uniformly, same as every other ownable leaf (see research.md Decision 1's
    # amendment: the PlayerOwnableWithConvenienceProtocol this section
    # originally specified was removed from the codebase).
```

- **Relationship**: a `PlayerState` owns many `UnitState`s (1:many). Per
  ARCHITECTURE.md §6 rule 1, the reference is stored on the "many" side —
  `UnitState.ownable.owned_by_player_id`, via the existing
  `PlayerOwnableMixin` (no new field type introduced; reuses `_PlayerOwnable`).
- **Validation**: `_PlayerOwnable.set_owner` is unconditional (no
  already-owned guard — that's a change from the original design; see
  research.md Decision 1's amendment). `release_owner()` still raises
  `NotYetOwnedResourceException` if the unit isn't currently owned. This
  feature does not call `.ownable.set_owner(...)` from any production code
  path itself (no "assign a new unit's owner at construction" flow exists
  yet in this codebase); it's exercised directly in test fixtures, the same
  way `PlanetState.assign_control` and `StrategyCardState`'s ownership
  fields are exercised only in tests today.
- **`UnitOwnershipError`** lives here, next to `UnitState`, rather than in
  `services/movement.py` — see data-model.md's `MovementService` section and
  research.md Decision 3 for why: it's a reusable "this player doesn't own
  this unit" type, not movement-specific.
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
class UnknownEntityError(GameError):
    """Base for every "no entity with this id exists" resolver failure."""
    entity_type: ClassVar[str] = "entity"

    def __init__(self, entity_id: str):
        super().__init__(f"No {self.entity_type} with id {entity_id!r} exists in this game.")

class UnknownSystemStateError(UnknownEntityError):
    entity_type: ClassVar[str] = "system state object"

class UnknownSystemConfigError(UnknownEntityError):
    entity_type: ClassVar[str] = "system config"

# ...plus UnknownPlayerError, UnknownDeployedUnitError, UnknownUnitConfigError,
# UnknownPlanetStateError, UnknownPlanetConfigError, UnknownFactionError -
# one pair per resolver method, not specific to this feature.

class GameStateResolver:
    def _get[T](self, entity_dict: Mapping[str, T], entity_id: str, error_cls: type[UnknownEntityError]) -> T:
        try:
            return entity_dict[entity_id]
        except KeyError:
            raise error_cls(entity_id) from None

    def resolved_system(self, system_id: str) -> ResolvedSystem:
        system_state = self._get(self._game_state.systems, system_id, UnknownSystemStateError)
        system_config = self._get(self._ruleset_config.systems, system_state.config_id, UnknownSystemConfigError)
        return ResolvedSystem(system_state, system_config)
```

> **Amendment (post-implementation)**: This originally specified
> `resolved_system` raising a bare `KeyError` on an unknown id, "caught and
> translated by `MovementService`." A follow-up pass instead generalized
> this to every `resolved_*` method via the shared `_get` helper above and
> the `UnknownEntityError` hierarchy — see research.md Decision 3. The
> resolver itself now raises the typed error; `MovementService` no longer
> catches anything for unknown ids.

## `MovementService` (`src/app/services/movement.py`) — MODIFIED (originally an empty stub)

```python
# app/services/movement.py
class MovementError(Exception):
    """Base for every rejection MovementService.move_unit can raise that's
    genuinely movement-specific (contrast UnknownDeployedUnitError/
    UnknownSystemStateError/UnitOwnershipError below, which generalized past
    this Service - see research.md Decision 3)."""

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
        resolved_unit = self._resolver.resolved_unit(unit_id)
        destination_system = self._resolver.resolved_system(destination_system_id)
        self._require_ownership(resolved_unit.state, requesting_player_id, UnitOwnershipError)
        ...
```

`UnknownDeployedUnitError`/`UnknownSystemStateError` come from
`app.resolved.game_state_resolver`; `UnitOwnershipError` comes from
`app.state.unit`; `_require_ownership` comes from `BaseService`
(`app.services.base`) — none of the three live in `movement.py` itself. See
research.md Decision 3 for the full rationale.

**Preconditions** (checked in this order — see research.md Decision 4):

1. `unit_id` resolves via `self._resolver.resolved_unit(unit_id)` → else `UnknownDeployedUnitError` (raised by the resolver itself).
2. `destination_system_id` resolves via `self._resolver.resolved_system(...)` → else `UnknownSystemStateError` (raised by the resolver itself).
3. `self._require_ownership(resolved_unit.state, requesting_player_id, UnitOwnershipError)` → else `UnitOwnershipError`.
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
