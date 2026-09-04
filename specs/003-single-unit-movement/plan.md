# Implementation Plan: Single-Unit Movement

**Branch**: `003-single-unit-movement` | **Date**: 2026-09-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-single-unit-movement/spec.md`

## Summary

Add `MovementService`, the codebase's first Domain Service, as a narrow
vertical slice: move one owned unit from its current system into a
hex-adjacent system, rejecting anything outside that scope (wrong owner,
non-adjacent/self/unknown destination, unknown unit) with distinguishable
errors. The technical approach composes the existing `GameStateResolver` +
`ResolvedUnit` with a new, equally minimal `ResolvedSystem`, closing two
small pre-existing gaps the slice exposes along the way: `UnitState` has no
ownership field yet, and `GameStateResolver` has no System accessor yet.

## Technical Context

**Language/Version**: Python 3.14 (per active `.venv`)

**Primary Dependencies**: Standard library only — no new third-party
dependency. Uses the existing `app.geometry.HexCoordinate.neighbors` for
adjacency.

**Storage**: N/A — in-memory `GameState`, no persistence changes beyond the
existing `Serializable` save/load contract on the fields touched.

**Testing**: pytest (`pytest==9.1.1`), run bare from repo root.

**Target Platform**: Cross-platform Python library (no OS-specific behavior).

**Project Type**: Single project — internal architectural layer (Domain
Services), not a standalone service/app.

**Performance Goals**: Not specified; a single move is O(1) dict lookups +
a 6-element adjacency check, negligible.

**Constraints**: One-way layering (`services` depends on `resolved`, never
touches raw `GameState`); State methods take only primitives, never Config
(ARCHITECTURE.md §1, §4).

**Scale/Scope**: One new Service (`MovementService`, one public method),
one new `Resolved*` class (`ResolvedSystem`), one new `GameStateResolver`
accessor, one new `UnitState` mixin composition, one new `GameState`
derived-filter method.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|---|---|---|
| I. Spec-Before-Code | PASS | `spec.md` already exists and precedes this plan. |
| II. Layered Architecture, One-Way Dependencies | PASS | `MovementService` (services/) depends only on `GameStateResolver` + `Resolved*` objects (resolved/); it never imports `app.state.game.GameState` or touches `game_state.deployed_units`/`game_state.systems` directly. `ResolvedSystem` depends only on `state/` + `config/`, matching `resolved`'s dependency direction. |
| III. Derive-Don't-Store | PASS | New relationship: a player owns many units → owner reference stored on each `UnitState` (the "many" side), never a `PlayerState.unit_ids` back-list — rule 1 in ARCHITECTURE.md §6. The new `GameState.units_in_system(system_id)` is a derived filter over `deployed_units`, not a stored/synced list. |
| IV. Config Immutability / State Mutability / Primitive-Only State Methods | PASS | `UnitState.place_in_system(system_id: str)` already takes a primitive; `MovementService` resolves Config at the Service layer and never passes a Config object down to State. Mixin decision test applied (§3): unit ownership reuses the existing `PlayerOwnableWithConvenienceProtocol` composition (no new mixin), because "owner" is already the exact vocabulary needed — same as `StrategyCardState`, no divergence to protect with a bespoke forwarding method (contrast `PlanetState`'s "control" vocabulary, which does diverge). |
| V. Test Coverage Before Completion | PASS (planned) | `tests/test_config` and `tests/test_state` continue to pass unmodified in structure (only sweep-covered automatically); new coverage added for every touched/new class in `tests/test_state` (updated) and new `tests/test_resolved`, `tests/test_services` packages — see Project Structure below. |

No violations requiring justification — Complexity Tracking is empty.

**Post-Phase-1 re-check**: Design artifacts (research.md, data-model.md,
contracts/, quickstart.md) introduced no new dependency, no new
State-to-State relationship beyond the one already justified above (unit
ownership), and no Config object crossing into State/Service method
signatures. All five rows above still hold as designed — no changes to this
table.

## Project Structure

### Documentation (this feature)

```text
specs/003-single-unit-movement/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md         # Phase 1 output
├── quickstart.md         # Phase 1 output
└── contracts/
    └── movement_service.md
```

### Source Code (repository root)

```text
src/app/
├── state/
│   ├── game.py            # MODIFIED: + units_in_system(system_id) derived filter
│   └── unit/unit.py        # MODIFIED: UnitState composes PlayerOwnableWithConvenienceProtocol
├── resolved/
│   ├── system.py           # NEW: ResolvedSystem(BaseResolvedObj[SystemState, SystemConfig])
│   └── game_state_resolver.py  # MODIFIED: + resolved_system(system_id)
└── services/
    └── movement.py         # MODIFIED (currently a stub): MovementService.move_unit(...) + exceptions

tests/
├── test_state/
│   ├── test_unit/test_unit.py   # MODIFIED: + ownership tests (mirrors test_planet.py/test_strategy.py)
│   └── test_game.py             # MODIFIED: + units_in_system tests
├── test_resolved/                # NEW package (pre-existing gap; scoped to what this feature adds)
│   ├── conftest.py               # NEW: session-scoped real-data ruleset_config fixture
│   ├── test_system.py            # NEW: ResolvedSystem construction
│   └── test_game_state_resolver.py  # NEW: resolved_system() only
└── test_services/                # NEW package
    ├── conftest.py               # NEW: ruleset_config + minimal two-system/one-unit game fixture
    └── test_movement.py          # NEW: one test per acceptance scenario + edge case
```

**Structure Decision**: Single-project layout, extending the existing
`src/app/{state,resolved,services}` / `tests/{test_state,test_resolved,test_services}`
mirror-structure convention (CLAUDE.md "Test layout"). `tests/test_resolved`
and `tests/test_services` don't exist yet; this feature creates them, scoped
strictly to the classes/methods this feature itself touches — the
pre-existing broader `tests/test_resolved` gap for `resolved_player`/
`resolved_unit`/`resolved_planet` (tracked in `specs/002-resolved-layer/plan.md`'s
open Principle V item) is not this feature's job to close.

## Complexity Tracking

*No Constitution Check violations — table intentionally empty.*
