# 0003. `Serializable` as the single save/load cooperative-chain terminal

**Status**: Accepted
**Date**: 2026-08-09 (approximate)

## Context

Every State class needs to save to and load from a plain dict, with trait
mixins (`Exhaustible`, `PlayerOwnableMixin`, etc.) each contributing their
own slice of the save data. This requires a cooperative `super()` chain
(each mixin calls up to the next), which needs a safe, shared terminal to
stop at — and needs *some* mechanism to guarantee every concrete leaf class
actually implements its half of the contract, since a forgotten override
here means silently-wrong save data, not an obvious crash.

Two designs were evaluated for that contract: `Protocol` (with a
`raise NotImplementedError` default body) versus `ABC` with
`@abstractmethod`.

## Decision

`Serializable` is a plain `ABC` with `@abstractmethod save`/
`init_from_save`, not a `Protocol`. Every State-layer class shares this one
common ancestor — a real inheritance tree, not cross-hierarchy structural
typing — so there's no need for `Protocol`'s duck-typing flexibility, and
`ABC` gives strictly stronger enforcement: a class missing a required
override fails at *construction* (`TypeError`), not merely the first time
the method happens to be *called*.

`load()` (via `cls.__new__(cls)` + `init_from_save`) is a single concrete
`classmethod` on `Serializable` — it never varies per class, so it needed no
separate `Loadable` protocol at all (an earlier design draft had one; see
`ARCHITECTURE.md` §3, "`Loadable` was retired").

## Consequences

**Easier**: a leaf class that forgets to implement `save`/`init_from_save`
fails immediately and loudly at the point of construction, with no way to
accidentally ship silently-incomplete save data.

**Harder**: `ABC` requires actual inheritance to satisfy the contract —
there's no structural/duck-typed escape hatch the way `Protocol` traits
elsewhere in this codebase allow (compare: Resolved-layer trait mixins,
which *do* need `Protocol` because they span Config-layer and State-layer
types with no common ancestor — `ARCHITECTURE.md` §3's mixin decision test).
This is a deliberate, narrower trade-off correct for `Serializable`
specifically, not a project-wide preference for `ABC` over `Protocol`.

## Alternatives considered

**`Protocol` with a `raise NotImplementedError` stub** — the design this
supersedes-in-spirit (never actually shipped, caught during design
discussion). Rejected: only catches a missing override the first time the
method is *called*, which could be arbitrarily late — a `Protocol` stub with
a silent `...`/`pass` body is worse still, since a forgotten override then
just silently returns wrong data with no error at all.

**Per-class hand-written `save`/`load`, no shared base** — rejected: loses
the cooperative-mixin composition entirely, forcing every leaf class to
duplicate every composed trait's save/load logic instead of each mixin
contributing its own slice once.
