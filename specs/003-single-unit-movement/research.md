# Phase 0 Research: Single-Unit Movement

No open `NEEDS CLARIFICATION` markers — the spec's Assumptions section
already resolves every scoping question a research pass would normally
raise. What's captured here are the concrete design decisions made while
translating the spec into a plan against the current, as-built state of
`src/app/{state,resolved,services}` (verified by reading the actual files,
not assumed from ARCHITECTURE.md alone).

## Decision 1: Unit ownership doesn't exist yet — add it via the existing `PlayerOwnableWithConvenienceProtocol`

**Finding**: `UnitState` (`src/app/state/unit/unit.py`) currently has no
owner field at all — only `config_id`/`instance_id` (via
`UUIDInstancedStateObj`), `location`, `current_damage`. FR-004 ("the Service
itself verifies the mover owns the unit") is unimplementable without one.

**Decision**: Compose `UnitState` with `PlayerOwnableWithConvenienceProtocol`
(`app.state.base.ownable`), the same way `StrategyCardState` already does —
not `PlayerOwnableMixin` + bespoke forwarding methods (the way `PlanetState`
does with "control", or `SpeakerTokenState` does with "speaker").

**Rationale**: ARCHITECTURE.md §3's mixin decision test for vocabulary:
compose with hand-written forwarding methods only when the domain
vocabulary *diverges* from generic "owner" language. A unit's owner is
already called "owner" everywhere in the spec and rules text — there's no
"controls"/"is assigned" distinction to protect, exactly the situation
`PlayerOwnableWithConvenienceProtocol` exists for (`StrategyCardState` is
the direct precedent, composing it with zero extra code).

**Alternatives considered**:
- Bespoke `assign_owner_player`/forwarding methods on `UnitState` — rejected,
  pure boilerplate with no vocabulary to protect.
- A new field `owner_player_id: str` with hand-rolled logic, bypassing
  `_PlayerOwnable` entirely — rejected, duplicates validation
  (`AlreadyOwnedResourceException` etc.) `_PlayerOwnable` already provides,
  and would be the first entity in the codebase not to reuse it.
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
distinguishable, catchable failures." The existing `GameStateResolver`
methods (`resolved_unit`, etc.) rely on plain dict `KeyError` for unknown
ids — not distinguishable enough on its own (a `KeyError` for an unknown
unit and a `KeyError` for an unknown system look identical to a caller
without inspecting the message).

**Decision**: `src/app/services/movement.py` defines one `MovementError`
base exception plus five concrete subclasses:

| Exception | Raised when | FR |
|---|---|---|
| `UnknownUnitError` | `unit_id` isn't in `game_state.deployed_units` | FR-006 |
| `UnknownSystemError` | `destination_system_id` isn't in `game_state.systems` | FR-006 |
| `UnitOwnershipError` | requesting player doesn't own the unit | FR-004 |
| `SelfMoveError` | destination is the unit's own current system | FR-005 |
| `IllegalDestinationError` | destination exists, isn't the unit's own system, but isn't hex-adjacent | FR-003 |

`MovementService.move_unit` catches the `KeyError`s from
`GameStateResolver.resolved_unit`/`resolved_system` at the boundary and
re-raises the matching typed error (`raise UnknownUnitError(...) from None`)
rather than letting a raw `KeyError` escape.

**Rationale**: A shared `MovementError` base lets a caller catch "any
movement rejection" in one clause when it doesn't care why, while each
subclass lets it branch on the specific reason when it does — exactly what
FR-008 asks for. Splitting FR-006 into two types (`UnknownUnitError` /
`UnknownSystemError`) rather than one shared `UnknownEntityError` costs
nothing and gives a strictly more useful signal to the caller than the spec
strictly requires (the spec only requires unknown-vs-outside-legal-set
distinguishability, not unit-vs-system).

**Alternatives considered**:
- Let `KeyError` propagate for unknown ids — rejected, not a distinguishable
  domain type, and indistinguishable from any other accidental `KeyError`
  bug in the call chain.
- One flat `IllegalMoveError(reason: str)` with a reason code/string —
  rejected: string-typed reasons are exactly the "stringly-typed" pattern
  CLAUDE.md's code-style guidance steers away from (enums/exception types
  over string discrimination) and are harder for a caller to `except` on
  selectively.

## Decision 4: Check ordering inside `move_unit`

**Decision**: unit exists → destination system exists → requester owns the
unit → destination isn't the unit's current system → destination is
hex-adjacent to the current system → mutate.

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
