# 0002. Derive-don't-store for State-to-State relationships

**Status**: Accepted
**Date**: 2026-08-07 (approximate)

## Context

State objects reference each other constantly (a unit is in a system, a
player has scored objectives, a planet is controlled by a player). The
naive approach — storing the relationship on both sides for convenient
lookup in either direction (`SystemState.unit_ids` *and*
`UnitState.system_id`) — creates two copies of the same fact that must be
kept in sync on every mutation, with no structural guarantee they ever
agree.

## Decision

Every State-to-State relationship stores a reference on exactly **one**
side, chosen by a fixed rule based on cardinality and optionality
(`ARCHITECTURE.md` §6: 1:many stores on the many; 1:optional stores on the
consistent side; many:many and optional:optional store on whichever side
"cares" about the relationship). The other direction is never stored — it's
computed on demand via a filter/query method (e.g.
`GameState.secret_objectives_held_by(player_id)`), never cached.

## Consequences

**Easier**: structurally impossible for the two "views" of a relationship to
disagree, since only one actually exists as stored data; no
mutation-ordering bugs from updating one side and forgetting the other.

**Harder**: reverse-direction queries cost an O(n) scan instead of an O(1)
lookup. Accepted as negligible given this project's realistic per-game
object counts (low thousands at most) — see the `slots=True` measurement in
`ARCHITECTURE.md` §2 for the same "is this optimization worth the
complexity" calculus applied to a related question.

## Alternatives considered

**Store both directions, sync on mutation** — rejected outright; this is the
exact failure mode the rule exists to prevent, and "remember to update both"
is not a structural guarantee, just a hope.

**Derived/cached index on `GameState`, invalidated on mutation** — considered
implicitly and rejected (see `ARCHITECTURE.md` §4's parallel "never
cache/store `Resolved*` objects" rule, same reasoning applied): a cache is
just the sync problem again, one level removed, with the added risk of
someone reading a stale value before invalidation runs.
