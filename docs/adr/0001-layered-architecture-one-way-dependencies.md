# 0001. Layered architecture with one-way dependencies

**Status**: Accepted
**Date**: 2026-08-06 (approximate — design phase preceding first commits)

## Context

The engine needs to represent both static ruleset data (unit stats, card
text, technologies — the same across every game) and live per-game data
(unit positions, player resources — different every game, mutating
constantly). Without an enforced boundary, code that needs "the current
value of X" tends to reach for whichever object is closest at hand,
producing tangled dependencies between static definitions and live state
that make the system hard to reason about, test in isolation, or later
expose behind an API boundary (the project's eventual goal — see README).

## Decision

Six layers, strict one-way dependencies: `data/` (raw YAML) → `config/`
(static, frozen, load-once) → `state/` (mutable, per-game) → `setup/`
(pre-game construction input) → `resolved/` (binds one State + its Config
for one operation) → `services/` (cross-entity rules logic) →
`orchestration/` (turn/phase sequencing). `geometry/` is shared,
dependency-free vocabulary any layer may import. A lower layer importing
from a higher one is a violation, not a style preference — enforced as
Constitution Principle II.

The orchestrator never touches raw `GameState` containers directly; it only
calls `Resolved*` objects and Domain Services.

## Consequences

**Easier**: each layer is independently testable with hand-built fixtures
(a `PlayerState` doesn't need a `RulesetConfig` to construct in isolation);
static and live data can never accidentally alias or drift against each
other; the eventual API-boundary goal (engine as a local server process) has
a natural seam to expose at, rather than requiring a retrofit.

**Harder**: every cross-layer interaction requires an explicit id-based
reference and a resolution step (see ADR 0002), which is more ceremony than
holding a direct object reference. Some operations that conceptually need
"a bit of everything" (e.g. constructing `GameState` from setup choices)
require careful placement to avoid violating the one-way rule — this
happened once in practice (an early `GameState.resolved_unit()` design
implicitly required `state/` to import `resolved/`; caught and corrected to
a `GameStateResolver` living in `resolved/` instead — see
`ARCHITECTURE.md` §1).

## Alternatives considered

**A single mutable domain model** (State objects holding live Config
references directly) — rejected: makes save/load, testing in isolation, and
multi-game sharing of `RulesetConfig` all substantially harder, per the
reasoning in `ARCHITECTURE.md` §3's `config_id`-not-object-reference rule.

**Fewer, coarser layers** (merge `resolved/` into `services/`, say) —
rejected: collapses the distinction between "binding one entity's own
State+Config" (cheap, no coordination) and "reasoning across multiple
entities" (real rules logic), which turned out to be a meaningful and
frequently-useful distinction once `services/` requirements started being
discussed (`ARCHITECTURE.md` §4–§5).
