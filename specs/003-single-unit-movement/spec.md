# Feature Specification: Single-Unit Movement

**Feature Branch**: `003-single-unit-movement`

**Created**: 2026-08-30

**Status**: Draft

**Input**: User description: "Add the first Domain Service, MovementService, as a narrow vertical slice: move a single unit from its current system to a hex-adjacent system. Scope is deliberately minimal — legality is based on physical hex adjacency only (no wormhole adjacency), anomaly movement restrictions are ignored, fleet composition/capacity/combat-trigger detection are out of scope, and the Service itself verifies the mover owns the unit. The goal is to establish the Services-layer pattern (composing GameStateResolver + multiple Resolved* objects) with the simplest possible real operation, ahead of a full MovementService spec."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Move a unit to an adjacent system (Priority: P1)

A player moves one of their units out of the system it currently occupies and into a different system that is a direct hex neighbor of it.

**Why this priority**: This is the minimal capability the whole feature exists to deliver — without it there is no Services-layer movement operation at all, and no way to validate that a Domain Service can correctly compose `GameStateResolver` output from multiple entities (unit, origin system, destination system) into one legal state change.

**Independent Test**: Can be fully tested by constructing a `GameState` with one player's unit deployed in system A, a second system B whose hex coordinate is a direct neighbor of A's, calling the move operation for that unit toward B, and asserting the unit's location now points at B (and no longer at A) while nothing else in the game state changed.

**Acceptance Scenarios**:

1. **Given** a unit deployed in system A, and system B is hex-adjacent to A, **When** the unit's owner requests a move of that unit to B, **Then** the unit's location updates to B and no other game data changes.
2. **Given** a unit deployed in system A with no other units present in system A, **When** the unit's owner requests a move of that unit to hex-adjacent system B, **Then** system A ends up with no units and system B ends up containing exactly that unit.

---

### User Story 2 - Reject moving a unit you don't own (Priority: P2)

A player attempts to move a unit that belongs to a different player, and the request is refused instead of silently repositioning someone else's unit.

**Why this priority**: This is the core turn-based safety guarantee for the whole feature — without it, any player could reposition any other player's units, which breaks the fundamental ownership model the rest of gameplay depends on. It's second (not first) because the rejection path only makes sense to define once the legal "happy path" it's rejecting an alternative to (User Story 1) exists.

**Independent Test**: Can be fully tested by constructing a unit owned by one player, requesting the move as a different player, and asserting the request is refused with a distinguishable error while the unit's location is unchanged.

**Acceptance Scenarios**:

1. **Given** a unit owned by Player Red deployed in system A, **When** Player Blue requests a move of that unit to hex-adjacent system B, **Then** the request is rejected and the unit remains in system A.

---

### User Story 3 - Move only takes effect within the current legal-destination set (Priority: P3)

A player requests to move a unit to a system that isn't one of the destinations this feature currently recognizes as legal (a direct hex neighbor), and the move does not take place.

**Why this priority**: "Legal destination" is deliberately a scoped, growable concept, not a fixed rule this feature declares forever. For this slice, direct hex neighbors are the only recognized source of legal destinations — not because any other system is permanently disallowed, but because other ways a system can become a legal destination (a matching wormhole, for instance) are simply not implemented yet and belong to a later feature. Ranked below ownership because this is a "not yet supported" boundary, not a security guarantee.

**Independent Test**: Can be fully tested by constructing a unit in system A and a system C that is not a direct hex neighbor of A, requesting a move of the unit to C, and asserting the move does not take place while the unit's location is unchanged.

**Acceptance Scenarios**:

1. **Given** a unit deployed in system A, and system C is not a direct hex neighbor of A, **When** the unit's owner requests a move of that unit to C, **Then** the move does not take place and the unit remains in system A, because C is not (yet) a recognized legal destination.

---

### Edge Cases

- What happens when the destination system id does not exist in the current game at all? → Rejected with an error distinguishable from "outside the legal-destination set" (an unknown destination is a different mistake than a real system that's simply not yet a recognized legal destination).
- What happens when the unit id being moved does not exist in the current game at all? → Rejected with a clear "unknown unit" error.
- What happens when the requested destination is the unit's own current system (a no-op "move")? → Rejected as an illegal move, not silently accepted as a no-op success.
- What happens when two systems are several hex rings apart but connected by a chain of adjacent systems? → The move does not take place — this feature's legal-destination set contains only direct hex neighbors (never transitive/multi-hop, and not yet wormhole-based); a chain of adjacent systems is not itself a path a unit can traverse in one move.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow a unit's owning player to move that unit from its current system to a different, real system that is a direct hex neighbor of its current system.
- **FR-002**: System MUST recognize direct hex-neighbor systems as legal move destinations. This is the current legal-destination set for this feature, not a permanent limit — other sources of legal destinations (e.g. matching wormhole links) are simply not part of this feature and are expected to extend the set in a later feature, not to be reconciled against a "non-adjacent is illegal" rule this feature does not assert.
- **FR-003**: System MUST NOT move a unit to a destination outside the current legal-destination set (for this feature, exactly its direct hex neighbors); the unit's location MUST remain unchanged when a requested destination falls outside that set.
- **FR-004**: System MUST reject a move request made by a player who does not own the unit being moved, and MUST leave the unit's location unchanged when it does.
- **FR-005**: System MUST reject a move request whose destination is the unit's own current system.
- **FR-006**: System MUST reject a move request that names a unit or destination system that does not exist in the current game, with the failure clearly distinguishable from a real destination/unit that simply falls outside the current legal-destination set.
- **FR-007**: A successful move MUST change only the moved unit's recorded location; it MUST NOT alter any other unit's location or ownership, or any other part of the game's state.
- **FR-008**: All rejections (FR-003 through FR-006) MUST be surfaced as distinguishable, catchable failures rather than a silent no-op, so a caller can tell *why* a move didn't happen.

### Key Entities

- **Unit**: The thing being moved. Has a current location (which system it occupies) and an owning player. Identified by an id unique within the current game.
- **System**: A place on the game map a unit can occupy. Identified by an id and a map position used to compute hex adjacency to other systems.
- **Player**: The actor requesting the move; a move is only legal when the requesting player owns the unit being moved.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every legal single-unit move between two hex-adjacent systems succeeds and is reflected in the unit's recorded location immediately after the request, with no unintended change to any other unit or player's data.
- **SC-002**: 100% of move attempts covered by this feature that don't satisfy its rules (wrong owner, destination outside the current legal-destination set, self-move, unknown unit or destination) leave the game state unchanged, and each failure reason is distinguishable from the others.
- **SC-003**: The movement capability is fully exercisable by an automated test that sets up nothing more than a minimal game with two hex-adjacent systems and one deployed unit — no dependency on turn-sequencing, tactical-action, or fleet-management capabilities that don't exist yet.

## Assumptions

- Wormhole-based adjacency (two systems with matching wormhole types counting as a legal destination regardless of hex distance) is out of scope for this slice; a follow-up feature *adds to* the legal-destination set to cover it — this feature does not assert that non-hex-neighbor systems are permanently illegal, only that this feature doesn't yet recognize them as legal.
- Anomaly movement effects (asteroid fields/supernovas blocking entry, nebula requiring the destination be the mover's active system, gravity rift risk of destruction) are out of scope for this slice; every hex-neighbor system is treated as uniformly enterable regardless of anomaly. A follow-up feature layers in anomaly rules, which may *remove* some hex-neighbor systems from the legal-destination set rather than add to it.
- Fleet-level concerns are out of scope: this feature moves exactly one unit at a time, and does not check destination fleet supply/capacity limits, tactical-action command-token spend, or "system already activated this round" rules.
- Combat triggers are out of scope: arriving in a system that already contains an opposing player's units is not detected or reacted to by this feature — it is only checked for adjacency, existence, and ownership legality.
- Ownership legality is checked by this feature itself (not deferred to a future orchestration layer), so the capability is safe to exercise directly — including from automated tests — without a caller having pre-verified who owns the unit.
- "Deployed unit" means a unit already present in the game and currently located in some system (not, e.g., already loaded in a cargo hold or resolved onto a planet); this feature does not re-validate whether that unit's type is allowed to independently occupy a system — that is assumed already enforced elsewhere.
- This is the first Domain Service the codebase will have; its shape is expected to set the pattern later services (combat, production, and others) follow, rather than being a one-off.
