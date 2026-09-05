---

description: "Task list for Single-Unit Movement (003)"
---

# Tasks: Single-Unit Movement

**Input**: Design documents from `/specs/003-single-unit-movement/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/movement_service.md, quickstart.md (all present)

**Tests**: Included as first-class tasks — the constitution's Principle V
("Test Coverage Before Completion") and CLAUDE.md's Testing section make
this a project-wide requirement, not an opt-in for this feature.

**Organization**: Grouped by user story (spec.md P1/P2/P3), on top of a
shared Foundational phase all three stories build on. `MovementService.move_unit`
is one cohesive method built up incrementally: US1 gets it moving units for
any resolvable, existence-checked request; US2 adds the ownership guard;
US3 adds the self-move and hex-adjacency legality guards. Each story's own
tests only exercise what that story adds, so each phase is still an
honest, independently-verifiable increment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no unmet dependencies)
- **[Story]**: US1 / US2 / US3, per spec.md's priorities
- Every task names its exact file path

## Path Conventions

Single project. Source under `src/app/`, tests mirror it 1:1 under `tests/`
(`tests/test_state`, `tests/test_resolved`, `tests/test_services`), per
CLAUDE.md's Test layout convention and plan.md's Project Structure.

---

## Phase 1: Setup

**Purpose**: Confirm a clean starting point — no scaffolding needed (no new
dependency, no new config; `tests/test_resolved/` and `tests/test_services/`
don't exist yet and are created by their own conftest tasks below).

- [X] T001 Run `pytest` from the repo root and confirm the existing suite
  (`tests/test_config`, `tests/test_state`) passes cleanly before making any
  change, so any later failure is attributable to this feature. (Found and
  fixed pre-existing stale-import breakage in
  `tests/test_config/test_objs/test_unit/test_valid_locations.py` — left
  over from a prior commit that moved `get_valid_locations_for` into
  `UnitConfig.valid_locations`; unrelated to this feature but blocked all
  collection. 641 passed after the fix.)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The shared building blocks every user story's tests and
implementation need — unit ownership, the `ResolvedSystem` binding, the
exception vocabulary, and the fixtures that construct a minimal movable
game. No user-story phase can be implemented before this completes.

- [X] T002 [P] Compose `UnitState` with `PlayerOwnableWithConvenienceProtocol`
  in `src/app/state/unit/unit.py` (mirrors `StrategyCardState` in
  `src/app/state/card/strategy.py`) — per data-model.md's `UnitState` section.
- [X] T003 Add ownership tests to
  `tests/test_state/test_unit/test_unit.py`: defaults to unowned,
  `assign_owner`/`is_owned_by_player`, `assign_owner` twice raises
  `AlreadyOwnedResourceException`, and a save/load round trip preserves
  ownership — mirroring `tests/test_state/test_planet.py`'s ownership tests.
  (Depends on T002.)
- [X] T004 [P] Create `ResolvedSystem(BaseResolvedObj[SystemState, SystemConfig])`
  in new file `src/app/resolved/system.py`, mirroring the `pass`-only body of
  `src/app/resolved/unit.py` — per data-model.md's `ResolvedSystem` section.
- [X] T005 Add `resolved_system(system_id: str) -> ResolvedSystem` to
  `src/app/resolved/game_state_resolver.py`, mirroring `resolved_planet`.
  (Depends on T004.)
- [X] T006 [P] Create `tests/test_resolved/conftest.py` with session-scoped
  `data_dir`/`ruleset_config` fixtures, mirroring
  `tests/test_config/conftest.py`'s `data_dir`/`ruleset_config`.
- [X] T007 [P] Create `tests/test_resolved/test_system.py`: construct a
  `ResolvedSystem` from a real `SystemConfig` id (via the `ruleset_config`
  fixture) and a hand-built `SystemState`, assert `.state`/`.config` bind
  correctly. (Depends on T004, T006.)
- [X] T008 [P] Create `tests/test_resolved/test_game_state_resolver.py`
  covering only the new `resolved_system(...)` method: resolves a real
  system, and raises `KeyError` for an unknown `system_id` (matching
  `resolved_unit`/`resolved_planet`'s existing unwrapped-`KeyError`
  behavior — translation into a domain error is `MovementService`'s job,
  not the resolver's). (Depends on T005, T006.)
- [X] T009 [P] Replace the `MovementService` stub in
  `src/app/services/movement.py` with the exception hierarchy only (no
  `move_unit` logic yet): `MovementError` base, plus `UnknownUnitError`,
  `UnknownSystemError`, `UnitOwnershipError`, `SelfMoveError`,
  `IllegalDestinationError` — per data-model.md / research.md Decision 3.
  Keep `MovementService(BaseService)` itself still a `pass`-body stub.
- [X] T010 Create `tests/test_services/conftest.py`: `data_dir`/
  `ruleset_config` session fixtures (mirroring T006), plus a fixture that
  builds a minimal `GameState` per quickstart.md's Setup section — two
  players (`red`, `blue`), three `SystemState`s (A and B mutually
  hex-adjacent via `HexCoordinate(...).neighbors`, C not adjacent to
  either), one `UnitState` in A owned by `red` via `unit.assign_owner("red")`
  — and wires up `GameStateResolver` + `MovementService` from them.
  (Depends on T002 for `assign_owner` to exist.)

**Checkpoint**: Foundation ready — `UnitState` has ownership, `ResolvedSystem`
+ resolver access exist, the exception vocabulary is defined, and
`tests/test_services/conftest.py` can hand every story's tests a working
`GameState` + `MovementService`.

---

## Phase 3: User Story 1 - Move a unit to an adjacent system (Priority: P1) 🎯 MVP

**Goal**: A resolvable, existence-checked move request relocates the unit
and changes nothing else in `GameState`.

**Independent Test**: Build a `GameState` with one unit in system A and a
hex-adjacent system B, call `move_unit` toward B, assert the unit is now in
B and only that field changed.

### Implementation for User Story 1

- [X] T011 [P] [US1] Add `units_in_system(system_id: str) -> tuple[UnitState, ...]`
  to `src/app/state/game.py`, filtering `deployed_units.values()` by
  `location.is_in_system and location.location_id == system_id` — per
  data-model.md Decision 5.
- [X] T012 [US1] Add tests for `units_in_system` to `tests/test_state/test_game.py`:
  empty for a system with no units, returns exactly the units located there,
  ignores units on a planet/ship with a matching `location_id` coincidence.
  (Depends on T011.)
- [X] T013 [US1] Implement the core of `MovementService.move_unit(*, unit_id,
  destination_system_id, requesting_player_id) -> None` in
  `src/app/services/movement.py`: resolve the unit via
  `self._resolver.resolved_unit(unit_id)`, catching `KeyError` →
  `UnknownUnitError`; resolve the destination via
  `self._resolver.resolved_system(destination_system_id)`, catching
  `KeyError` → `UnknownSystemError`; then unconditionally
  `resolved_unit.state.place_in_system(destination_system_id)` — ownership
  and destination-legality guards are added in later phases, not here.
  (Depends on T004, T005, T009.)
- [X] T014 [US1] Create `tests/test_services/test_movement.py` with: Acceptance
  Scenario 1 (move to adjacent system B succeeds; snapshot `game_state.save()`
  before/after and assert the only difference is the unit's `location`),
  Acceptance Scenario 2 (`units_in_system(A) == ()` and
  `units_in_system(B) == (unit,)` after the move), edge case unknown unit id
  → `UnknownUnitError`, edge case unknown destination id → `UnknownSystemError`.
  (Depends on T010, T012, T013.)

**Checkpoint**: User Story 1 is fully functional and independently testable
— a valid move works end-to-end and unknown ids are rejected distinguishably.

---

## Phase 4: User Story 2 - Reject moving a unit you don't own (Priority: P2)

**Goal**: A move requested by a player who doesn't own the unit is refused,
unit stays put.

**Independent Test**: Unit owned by `red`, request the move as `blue`,
assert `UnitOwnershipError` and the unit's location is unchanged.

### Implementation for User Story 2

- [X] T015 [US2] Add the ownership guard to `MovementService.move_unit` in
  `src/app/services/movement.py`: after both resolutions succeed (T013),
  before the mutation, raise `UnitOwnershipError` when
  `not resolved_unit.state.is_owned_by_player(requesting_player_id)` — per
  contracts/movement_service.md's check ordering. (Depends on T013.)
- [X] T016 [US2] Add to `tests/test_services/test_movement.py`: Acceptance
  Scenario 1 (unit owned by `red`, move requested as `blue`, raises
  `UnitOwnershipError`). Assert via a `game_state.save()` snapshot taken
  before the call and compared after that nothing in `GameState` changed —
  not just that the unit's own location is still A — per FR-007/SC-002 and
  matching T014's snapshot-diff pattern. (Depends on T015.)

**Checkpoint**: User Stories 1 and 2 both independently functional.

---

## Phase 5: User Story 3 - Move only within the current legal-destination set (Priority: P3)

**Goal**: A destination that isn't the unit's own system and isn't a direct
hex neighbor is refused; a self-move is refused distinguishably from that.

**Independent Test**: Unit in A; request a move to non-adjacent system C →
rejected; request a move to A itself → rejected with a different error type.

### Implementation for User Story 3

- [X] T017 [US3] Add the self-move and hex-adjacency guards to
  `MovementService.move_unit` in `src/app/services/movement.py`, after the
  ownership guard (T015) and before the mutation: raise `SelfMoveError` when
  `destination_system_id == resolved_unit.state.location.location_id`;
  otherwise resolve the origin system via
  `self._resolver.resolved_system(resolved_unit.state.location.location_id)`
  and raise `IllegalDestinationError` when
  `destination_system.state.map_hex_coordinate not in origin_system.state.map_hex_coordinate.neighbors`.
  (Depends on T015.)
- [X] T018 [US3] Add to `tests/test_services/test_movement.py`: Acceptance
  Scenario 1 (move to non-adjacent system C raises `IllegalDestinationError`),
  edge case self-move to A raises `SelfMoveError`, edge case a system two
  hex rings away reachable only via an intermediate adjacent system still
  raises `IllegalDestinationError` (no multi-hop traversal). For the
  Acceptance Scenario 1 case, assert via a `game_state.save()` snapshot
  taken before the call and compared after that nothing in `GameState`
  changed — not just that the unit's own location is still A — per
  FR-007/SC-002 and matching T014's snapshot-diff pattern. (Depends on T017.)
  (Note: reused system C, moved to be a neighbor of B but not of A, so it
  doubles as both the plain non-adjacent destination and the multi-hop-chain
  edge case, rather than adding a 4th system — see conftest.py.)

**Checkpoint**: All three user stories independently functional — the full
contract in contracts/movement_service.md is implemented.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T019 [P] Run `pytest` bare from the repo root; confirm
  `tests/test_config` and `tests/test_state` (constitution Principle V gate)
  plus the new `tests/test_resolved` and `tests/test_services` all pass
  cleanly together. (661 passed, 0 failed.)
- [X] T020 [P] Walk quickstart.md's validation table row by row against the
  actual test run and check off each row (including the explicit
  before/after `game_state` snapshot comparison for a rejection case).
- [X] T021 Review ARCHITECTURE.md against what was actually built (the new
  `ResolvedSystem`/`GameStateResolver.resolved_system`, `UnitState` ownership,
  `GameState.units_in_system`, and this codebase's first Domain Service) and
  update it if implementation diverged from research.md's decisions, per
  CLAUDE.md's "update it when a design decision changes." (No divergence
  from research.md's decisions; added a new "Worked example: MovementService"
  subsection to §5 capturing the exception-hierarchy and guard-clause-
  ordering conventions this feature establishes as the pattern for future
  Domain Services, per the spec's explicit intent.)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup. Blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational only.
- **User Story 2 (Phase 4)**: Depends on Foundational + T013 (extends the
  same `move_unit` method US1 started) — not independent of US1's code, but
  independently *testable* (its own test only exercises the ownership path).
- **User Story 3 (Phase 5)**: Depends on Foundational + T015 (extends the
  guard chain US2 continued) — same relationship as US2→US1.
- **Polish (Phase 6)**: Depends on all three user stories.

Note: unlike a typical spec-kit feature where stories touch disjoint files
and can be built in parallel by different people, US1/US2/US3 here all
extend one method (`MovementService.move_unit`) as sequential guard clauses
— per research.md Decision 4's fixed check ordering (existence → ownership
→ self-move/adjacency → mutate). They must be implemented in priority order
(P1 → P2 → P3), not in parallel with each other, even though each has its
own independent test.

### Within Each Phase

- Foundational: T002→T003, T004→T005, (T004,T006)→T007, (T005,T006)→T008,
  T002→T010 are the only real chains; T002, T004, T006, T009 have no
  prerequisites and can start immediately together.
- Each user story: implementation task before its test task (nothing here
  was scoped as test-first, since this project's convention — see
  `tests/test_state/test_planet.py` etc. — is tests alongside/after the
  behavior, not a strict red-green-refactor requirement).

### Parallel Opportunities

- T002, T004, T006, T009 can all start together right after T001.
- T007 and T008 can run in parallel once their respective prerequisites
  (T004+T006, T005+T006) are done.
- T019 and T020 can run in parallel at the end.

---

## Parallel Example: Foundational Phase

```bash
# After T001, launch these four together (different files, no shared deps):
Task: "Compose UnitState with PlayerOwnableWithConvenienceProtocol in src/app/state/unit/unit.py"
Task: "Create ResolvedSystem in src/app/resolved/system.py"
Task: "Create tests/test_resolved/conftest.py with data_dir/ruleset_config fixtures"
Task: "Replace the MovementService stub's body with the exception hierarchy in src/app/services/movement.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: Setup (T001).
2. Phase 2: Foundational (T002–T010) — CRITICAL, blocks everything else.
3. Phase 3: User Story 1 (T011–T014).
4. **STOP and VALIDATE**: `pytest tests/test_services/test_movement.py -v`
   passes; a valid adjacent move works end-to-end with distinguishable
   unknown-id errors. This alone is a legitimate, demoable MovementService
   slice, even before ownership/legality guards exist.

### Incremental Delivery

1. Setup + Foundational → foundation ready.
2. Add User Story 1 → test independently → MVP.
3. Add User Story 2 → test independently → ownership now enforced.
4. Add User Story 3 → test independently → full contract in
   contracts/movement_service.md now implemented.
5. Polish (T019–T021) → full-suite verification + docs review.

---

## Notes

- [P] tasks touch different files with no unmet dependency at the time they
  start.
- `MovementService.move_unit`'s guard clauses are added in a fixed order
  across US1→US2→US3 (see research.md Decision 4) — do not reorder them
  when implementing, since `SelfMoveError` must be raised before the
  adjacency check would otherwise also (correctly, but less specifically)
  reject a self-move as `IllegalDestinationError`.
- Every rejection path must leave `GameState` completely unchanged — verify
  this explicitly with a snapshot/diff in at least one test per phase, not
  merely by checking the unit's own location.
