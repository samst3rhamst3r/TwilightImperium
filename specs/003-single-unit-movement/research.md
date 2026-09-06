# Phase 0 Research: Single-Unit Movement

No open `NEEDS CLARIFICATION` markers — the spec's Assumptions section
already resolves every scoping question a research pass would normally
raise. What's captured here are the concrete design decisions made while
translating the spec into a plan against the current, as-built state of
`src/app/{state,resolved,services}` (verified by reading the actual files,
not assumed from ARCHITECTURE.md alone).

## Decision 1: Unit ownership doesn't exist yet — add it via `PlayerOwnableMixin`

**Finding**: `UnitState` (`src/app/state/unit/unit.py`) currently has no
owner field at all — only `config_id`/`instance_id` (via
`UUIDInstancedStateObj`), `location`, `current_damage`. FR-004 ("the Service
itself verifies the mover owns the unit") is unimplementable without one.

**Decision**: Compose `UnitState` with `PlayerOwnableMixin`
(`app.state.base.ownable`), the same way `StrategyCardState`, `PlanetState`,
`SecretObjectiveCardState`, and the special tokens all do.

> **Amendment (post-implementation)**: The original version of this decision
> composed a `PlayerOwnableWithConvenienceProtocol` that forwarded generic
> `assign_owner`/`is_owned_by_player`/etc. directly onto the leaf class, on
> the theory that "owner" vocabulary never diverges enough to need it. That
> Protocol was removed from the codebase in a later pass: it turned out to
> be the *only* consumer of the convenience-forwarding idea (every other
> ownable leaf either has bespoke vocabulary already, like `PlanetState`'s
> "control", or is fine reached via `.ownable.*` directly), so keeping a
> whole extra mixin alive for one case wasn't worth it. The uniform access
> pattern that replaced it — every ownable leaf, bespoke vocabulary or not,
> exposes ownership through its own `.ownable: _PlayerOwnable` field, and
> callers (including `MovementService`, via the new shared
> `BaseService._require_ownership` helper) always go through `.ownable.*`
> rather than through a leaf-level convenience method — is simpler and more
> consistent, so `UnitState` follows it too: no forwarding methods of its
> own, just `PlayerOwnableMixin` and direct `.ownable.*` access.

**Rationale**: ARCHITECTURE.md §3's mixin decision test for vocabulary still
applies to the underlying choice (compose, don't inherit, when leaf classes
might want divergent vocabulary) — `UnitState` doesn't need bespoke
vocabulary any more than it originally did, it just now reaches the shared
mechanism the same uniform way every other ownable leaf does, rather than
through a since-removed convenience layer.

**Alternatives considered**:
- Bespoke `assign_unit_owner`/forwarding methods on `UnitState` — rejected,
  pure boilerplate with no vocabulary to protect.
- A new field `owner_player_id: str` with hand-rolled logic, bypassing
  `_PlayerOwnable` entirely — rejected, would duplicate the single canonical
  `owned_by_player_id`/`is_owned_by_player` lookup `_PlayerOwnable` already
  provides, and would be the first entity in the codebase not to reuse it.
- Storing ownership as a reverse list on `PlayerState` (`unit_ids: set[str]`)
  — rejected outright by ARCHITECTURE.md §6 rule 1 (1:many → store on the
  "many" side, i.e. on each unit, not a synced list on the player).

## Decision 2: Build `ResolvedSystem` now, not a plain-State accessor

**Finding**: `GameStateResolver` currently exposes `resolved_player`,
`resolved_unit`, `resolved_planet` — no System accessor of any kind.
`SystemConfig` exists and is a real, resolvable Config for every System, so
this is not a "genuinely no Config" case (contrast the plain-accessor half
of Resolved-layer Rule 1). No method this feature writes actually reads
`SystemConfig` fields yet (adjacency is computed purely from
`SystemState.map_hex_coordinate`).

**Decision**: Add a new, minimal `ResolvedSystem(BaseResolvedObj[SystemState, SystemConfig])`
with no body beyond the generic base (`pass`), plus
`GameStateResolver.resolved_system(system_id) -> ResolvedSystem`, and have
`MovementService` resolve both the origin and destination systems through
it.

**Rationale**: Two things point the same direction here. First, precedent:
`ResolvedUnit` and `ResolvedPlanet` are themselves `pass`-only bodies today
— ARCHITECTURE.md §4 explicitly endorses building a `Resolved*` type ahead
of a concrete Config-reading method when a real, near-term need already
exists ("`ResolvedUnit` was justified immediately — movement, combat both
need it"). Second, the feature's own stated purpose is to "establish the
Services-layer pattern (composing `GameStateResolver` + multiple `Resolved*`
objects)" — a plain `SystemState` accessor would technically work for
*this* slice's adjacency check, but would misrepresent System as a
no-Config entity (it isn't) and dodge the exact pattern this feature exists
to establish, one `MovementService` follow-ups (wormhole adjacency, anomaly
rules) will need `SystemConfig` for immediately.

**Alternatives considered**:
- `GameStateResolver.system_state(system_id) -> SystemState` plain accessor
  — rejected: System has real Config, so this would apply the "no Config"
  half of Rule 1 to an entity that doesn't qualify for it, and would need to
  be redone the moment a follow-up feature needs `SystemConfig` (wormhole
  type, anomaly type).
- Reaching into `GameState.systems[...]` directly from `MovementService` —
  rejected outright: violates Rule 1 (Services reach State only through
  `GameStateResolver`).

## Decision 3: Custom exception hierarchy, one type per distinguishable rejection

**Finding**: FR-008 requires FR-003 through FR-006 to each be "surfaced as
distinguishable, catchable failures." `GameStateResolver`'s methods relied on
plain dict `KeyError` for unknown ids — not distinguishable enough on its
own (a `KeyError` for an unknown unit and a `KeyError` for an unknown system
look identical to a caller without inspecting the message).

**Decision** *(post-implementation amendment — see note below)*: The
hierarchy ended up split across three modules instead of living entirely in
`movement.py`, because two of the five rejection reasons generalized past
this one Service once they were actually implemented:

- **`src/app/errors.py`** (new) — `GameError(Exception)`, an app-wide base.
  Everything below inherits it, including `MovementError` itself (fixed
  after an initial pass briefly left it extending plain `Exception`).
- **`src/app/resolved/game_state_resolver.py`** — `UnknownEntityError(GameError)`
  (a `ClassVar[str] entity_type`, message built from `entity_id` alone), plus
  one subclass per (container, id-namespace) pair across *every* resolver
  method, not just this feature's two: `UnknownPlayerError`,
  `UnknownDeployedUnitError`, `UnknownUnitConfigError`,
  `UnknownSystemStateError`, `UnknownSystemConfigError`,
  `UnknownPlanetStateError`, `UnknownPlanetConfigError`, `UnknownFactionError`.
  A generic `GameStateResolver._get[T](entity_dict, entity_id, error_cls)`
  helper does the lookup and raises `error_cls(entity_id)` on `KeyError`;
  every `resolved_*` method (including `resolved_system`) now uses it, so
  `MovementService` no longer catches anything for unknown ids at all — it
  just calls `resolved_unit`/`resolved_system` and lets
  `UnknownDeployedUnitError`/`UnknownSystemStateError` propagate.
- **`src/app/state/base/ownable.py`** — `OwnershipError(GameError)`, a
  generic "wrong owner" type taking `(entity_id, actual_owner_id)`.
- **`src/app/state/unit/unit.py`** — `UnitOwnershipError(OwnershipError)`
  (`entity_name = "unit"`), the concrete type raised for FR-004. It lives
  next to `UnitState`, not in `movement.py`, since "is this unit owned by
  this player" is reusable by any future Service, not movement-specific.
- **`src/app/services/base.py`** — `BaseService._require_ownership(entity, player_id, error_cls)`,
  a shared helper: checks `entity.ownable.is_owned_by_player(player_id)` and
  raises `error_cls(entity.id, entity.ownable.owned_by_player_id)` if not.
  `move_unit` calls
  `self._require_ownership(resolved_unit.state, requesting_player_id, UnitOwnershipError)`.
- **`src/app/services/movement.py`** now defines only what's genuinely
  movement-specific: `MovementError` (base) plus `SelfMoveError` and
  `IllegalDestinationError`.

| Exception | Lives in | Raised when | FR |
|---|---|---|---|
| `UnknownDeployedUnitError` | `app.resolved.game_state_resolver` | `unit_id` isn't in `game_state.deployed_units` | FR-006 |
| `UnknownSystemStateError` | `app.resolved.game_state_resolver` | a system id (destination, or the unit's own current system) isn't in `game_state.systems` | FR-006 |
| `UnitOwnershipError` | `app.state.unit` | requesting player doesn't own the unit | FR-004 |
| `SelfMoveError` | `app.services.movement` | destination is the unit's own current system | FR-005 |
| `IllegalDestinationError` | `app.services.movement` | destination exists, isn't the unit's own system, but isn't hex-adjacent | FR-003 |

**Rationale**: The original design put all five types in `movement.py`
under one `MovementError` base so a caller could catch "any movement
rejection" in one clause. Once actually built, two of the five turned out to
answer a question every `resolved_*` call has (not just movement's two), so
generalizing them to the resolver layer — the one place every Service
already goes through (Rule 1) — avoided re-solving "unknown id" per-Service
the moment a second Service needed it. `UnitOwnershipError` generalizes the
same way, paired with the shared `_require_ownership` helper, since "does
this player own this unit" is not a movement-only question either (a future
`CombatService` checking the same thing would otherwise need its own copy).
The trade-off: a caller can no longer catch "any movement rejection" with a
single `except MovementError` — the five types are no longer siblings under
one base. FR-008's actual requirement (each reason distinguishable and
independently catchable) still holds; it's satisfied by five cross-cutting
types now instead of five siblings.

**Alternatives considered** (unchanged from the original decision):
- Let `KeyError` propagate for unknown ids — rejected, not a distinguishable
  domain type, and indistinguishable from any other accidental `KeyError`
  bug in the call chain.
- One flat `IllegalMoveError(reason: str)` with a reason code/string —
  rejected: string-typed reasons are exactly the "stringly-typed" pattern
  CLAUDE.md's code-style guidance steers away from (enums/exception types
  over string discrimination) and are harder for a caller to `except` on
  selectively.

**Note on this amendment**: Revised after initial implementation, once a
follow-up pass generalized unknown-id and ownership handling across the
resolver/state layers (see `src/app/errors.py`'s introduction in the
project's git history). This section now reflects the as-built shape rather
than the original Phase-0 plan, per this project's "specs are source of
truth, not scratch notes" convention (constitution, Principle I).

## Decision 4: Check ordering inside `move_unit`

**Decision**: unit exists → destination system exists → requester owns the
unit → destination isn't the unit's current system → destination is
hex-adjacent to the current system → mutate.

> **Amendment (post-implementation)**: The first two checks are no longer
> explicit `try`/`except` blocks inside `move_unit` — per Decision 3, they're
> now enforced automatically by `GameStateResolver.resolved_unit`/
> `resolved_system` themselves. `move_unit` just calls
> `self._resolver.resolved_unit(unit_id)` and
> `self._resolver.resolved_system(destination_system_id)` unconditionally at
> the top and lets `UnknownDeployedUnitError`/`UnknownSystemStateError`
> propagate. The *order* is unchanged (existence still precedes
> ownership/legality) — only the mechanism moved from Service-level
> `try`/`except` + re-raise to resolver-level built-in behavior.

**Rationale**: Existence checks must precede everything else (ownership and
adjacency are meaningless to evaluate against ids that don't resolve to
anything). Self-move is checked as its own guard *before* the adjacency
check specifically so it raises `SelfMoveError` rather than falling through
to `IllegalDestinationError` — a system is never its own hex neighbor, so
without this explicit guard a self-move would still be correctly *rejected*,
just under the wrong, less-informative exception type, undermining Decision
3's per-reason distinguishability. This ordering does not correspond to the
spec's user-story *priority* order (P1/P2/P3 is about build/test priority,
not runtime check order) — ownership (P2) is checked before the
legal-destination-set check (P3) here only because it happens to come first
in the natural existence→identity→geometry progression, not because P2
outranks P3 at runtime.

## Decision 5: `GameState.units_in_system(system_id)` — new derived filter

**Finding**: Acceptance Scenario 2 requires asserting "system A ends up
with no units and system B ends up containing exactly that unit" — but
`SystemState` stores no unit list (correctly, per ARCHITECTURE.md §6 — units
already store their system via `location`), and `GameState` has no existing
query to derive "units currently in system X" from `deployed_units`.

**Decision**: Add `GameState.units_in_system(system_id: str) -> tuple[UnitState, ...]`,
filtering `self.deployed_units.values()` by
`location.is_in_system and location.location_id == system_id`.

**Rationale**: Matches the established derive-don't-store pattern (§6) for
"many" queries — computed on demand from the single source of truth
(`UnitState.location`), never a stored/synced list. It's also the cleanest
way to express Acceptance Scenario 2's own assertion, and is a small,
obviously-reusable primitive (stacking-limit checks, combat-detection in a
system, future fleet composition — all mentioned as *out of scope* for this
feature but as things a later feature will want exactly this filter for).

**Alternatives considered**:
- Filter `deployed_units.values()` inline inside the test only, no new
  `GameState` method — rejected: this is a "does this need only this
  entity's own already-known data" query at exactly `GameState`'s level
  (ARCHITECTURE.md §1 table), the same shape as the existing `system_at`
  method; leaving it as ad hoc test-only logic would duplicate itself the
  moment a second caller (a future Service) needs the same query.

## Scope boundary carried forward from the spec's Assumptions (not re-litigated here)

Wormhole adjacency, anomaly movement restrictions, fleet
capacity/supply/command-token checks, and combat-trigger detection are all
explicitly out of scope per the spec's Assumptions section — `MovementService.move_unit`
does not check any of them, and this plan does not introduce any
scaffolding (empty methods, TODO hooks) anticipating them, per the
project's general practice of not building ahead of a real, current need.
