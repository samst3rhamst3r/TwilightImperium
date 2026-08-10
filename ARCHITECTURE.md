# Twilight Imperium App — Architecture Decisions

This document summarizes the layering, naming, and design conventions established
for the app. It's meant as durable reference context (e.g. for Claude Code), not
a tutorial — see inline rationale where it clarifies *why*, not just *what*.

## 1. Layer overview

```
data/        raw YAML content (no code)
config/      Config objects: static, load-once, shared across all games
state/       State objects: mutable, per-game, live game data
resolved/    Resolved objects: thin per-operation binding of one State + its Config
services/    Domain Services: heterogeneous, cross-entity rules logic
orchestration/  sequencing/flow — decides *when* things happen
geometry/    hex coordinate math — no dependencies on any other layer
```

Dependency direction is one-way: `resolved` depends on `config` + `state`;
`services` depend on `resolved`; `orchestration` depends on `services`. Lower
layers never import from higher ones. `geometry` and `config/enums.py` are
shared vocabulary/types that any layer may import — that's importing a *type*,
not coupling to *data*, so it doesn't violate the boundary.

**The orchestrator never touches raw `GameState` containers directly.** It only
calls `Resolved*` objects and Domain Services. `GameState`'s containers are
effectively private; `GameState.resolved_*()` factory methods are the only
sanctioned access point.

## 2. Config layer

- `RulesetConfig` is the static-data aggregate: loaded once (`RulesetConfig.load(config_dir)`),
  shared across every concurrent `GameState`, independent of any specific game
  (independent of player count, factions chosen, etc.). Frozen/immutable.
- Per-type loader functions (`load_strategy_card_configs`, etc.) live in
  `config/loader.py`, each returning a list of **already-typed Config objects**
  (never raw dicts) — loaders own "YAML shape → typed object," `RulesetConfig.load`
  only composes the results.
- `RulesetConfig` builds `MappingProxyType` indices (ID → object) in `__post_init__`
  for O(1) lookup, alongside the ordered tuple form if needed.
- Config classes use trait mixins for optional fields (`RequiresFunctionalText`,
  `RequiresFlavorText`, `RequiresFlavorTextOptions`) — composed per card type as needed.
- Enums (`UnitClass`, `TechnologyType`, etc.) live in `config/enums.py` — static
  vocabulary, imported freely by State/Resolved without violating layering.
- `HexCoordinate` (from `geometry/`) is imported into Config the same way — a shared
  value type, not a data-coupling.
- Naming: settled on **`RulesetConfig`**, not `GameConfig` — signals "static ruleset,"
  not "belongs to one game."

## 3. State layer

- State objects are mutable, per-game data containers, referencing Config only by
  **`config_id: str`** — never a direct Config object reference (serialization,
  aliasing-safety, equality-simplicity, testability).
- State methods take **primitives/already-decided values**, never Config objects.
  Any computation requiring Config moves up to the Resolved layer, which resolves
  Config and calls the simpler State method with a concrete value.
  - e.g. not `unit.can_move_to(terrain, unit_config)` → prefer computing at Resolved
    layer from `self.config`, or if the State method must decide legality itself,
    pass a plain value it needs, not the Config object.
- StrEnums (not raw strings) for closed categorical fields (`PlayerColor`, `GamePhase`,
  etc.) — type safety, exhaustiveness checking, no stringly-typed bugs.

### Mixin pattern: dataclass mixin vs. Protocol vs. ABC

Decision test:
- **Needs to *store* real data / be composed with `default_factory`?** → concrete
  dataclass mixin (e.g. `PlayerOwnable`, `ExhaustableStateMixin`).
- **Only declares a required shape, no data of its own, used across *unrelated*
  class families with no common ancestor** (e.g. Config-layer + Resolved-layer
  traits)? → `Protocol`.
- **Every implementer already shares one common concrete ancestor, and the method
  signature is uniform?** → prefer `ABC` + `@abstractmethod` over `Protocol` — gives
  real **construction-time** enforcement (`TypeError` if unimplemented), stronger
  than `Protocol`'s call-time (`NotImplementedError`) or static-only (`mypy`) checks.

**Composition over inheritance** for mechanism-sharing mixins whose *generic verb
names* shouldn't leak onto the leaf class's public surface:
- `PlayerOwnable` (`owner_player_id`, `assign_owner`/`remove_owner`) is *composed*
  as a field (`ownership: PlayerOwnable`) rather than inherited, because different
  leaf types use different domain vocabulary for the same mechanism — a Planet is
  "controlled" (`assign_control`), a Speaker Token is "assigned" (`assign_speaker`).
  Each leaf writes its own thin, domain-named forwarding method to
  `self.ownership.assign_owner(...)`. This avoids leaking the generic method name
  onto every leaf's public API.
- `Exhaustable` was **collapsed directly into `ExhaustableStateMixin`** (inherited,
  not composed) because "exhaust"/"ready" terminology never diverges across entity
  types in this game — no vocabulary to protect, so composition's benefit doesn't
  apply. Rule of thumb: compose when vocabulary varies by leaf type; inherit
  directly when it doesn't.
- Where multiple leaf types want the *same* generic vocabulary (no divergence),
  a `Protocol` convenience mixin (e.g. `HasOwnership`) can supply default
  forwarding methods (`assign_owner`) — leaf classes needing generic vocab inherit
  both the storage mixin *and* the convenience Protocol; leaf classes needing
  custom vocab inherit only the storage mixin and write their own forward.

### `StateBase` — single shared terminal / ABC root

- All per-field "cooperative super() chains" (save/load) terminate at one shared
  `StateBase`, not multiple competing terminal classes. Consolidating into one
  avoids silently-incomplete chains (a mixin's `super()` call reaching an
  unintended, differently-scoped terminal).
- `StateBase` implements `Savable`/`MixinInitializer`'s contract concretely
  (`to_save_dict`, `init_from_save_dict`) — as **`ABC` + `@abstractmethod`**, not
  `Protocol`, since every State-layer class already shares this one common
  ancestor (real inheritance tree, not cross-hierarchy structural typing).
- **`Loadable` was retired** — its one implementation (`load`: `cls.__new__(cls)`
  + `obj.init_from_save_dict(data)`) never varies per class, so it's just a plain
  concrete method on `StateBase`, not a separate Protocol.
- `to_save_dict`/`init_from_save_dict` **do** stay as genuinely overridden,
  cooperative (`super()`-chained) methods — each trait mixin and leaf class
  contributes its own slice, chaining up through `StateBase`'s no-op terminal.
  This is real per-class variation, unlike `load`.

### `new_game` vs. `load` — different problems, different mechanisms

- **`load(data: dict)`**: needs `cls.__new__(cls)` (bypasses `__init__` entirely)
  because it receives an **opaque nested dict** that must be unpacked/reconstructed
  per-field — cooperative `init_from_save_dict` chaining is real, necessary work here.
- **`new_game(...)`**: called with **already-typed, named arguments** at the call
  site. Once every required field (e.g. `config_id`) is a real, explicit parameter,
  plain `cls(config_id=..., ...)` works directly — **no `__new__` bypass or
  cooperative chain needed**. Dataclass inheritance already merges every base
  class's fields into one generated `__init__`, so composed/inherited mixin
  fields (including `default_factory` ones) populate correctly for free.
- Every leaf class implements its **own** `new_game(...)` with concrete, documented
  parameters — this is a deliberate design choice: it forces per-class documentation
  of exactly what setup data that entity needs, with no shared/generic default to
  hide behind.
- Field-default gotcha (verified): a bare `cls.__new__(cls)` (no `__init__` run)
  only gets a field's value "for free" if it's a **plain literal default**
  (Python sets those as a class-attribute fallback). Fields using
  `default_factory=...` or no default at all do **not** survive `__new__` —
  they raise `AttributeError` until explicitly set. This only matters for the
  `load` path; the `new_game` path avoids it entirely by using `cls()` directly.
- `instance_id` uses `field(default_factory=lambda: str(uuid4()))` — not a
  required no-default field — specifically so trivial "no real setup needed"
  leaf classes can construct via plain `cls()` with zero required arguments where
  appropriate.

### `__post_init__` — when it's appropriate

Test: *"If I explicitly pass a value for this field to the constructor, does
`__post_init__`'s logic respect it, or silently clobber it?"* — if clobber, it
doesn't belong in `__post_init__`.

- **Good fit**: purely structural derivations from already-provided sibling
  fields, with no legitimate independent value a caller could want instead.
  - `RulesetConfig._strategy_card_index` built from `self.strategy_cards`.
  - `PlayerState.command_token_reinforcement_pool = 16 - (tactic + fleet + strategy)`
    — always must be synchronized to the other three pools, regardless of
    construction path (new game, loaded game, etc.), pure arithmetic, no
    domain-rule branching, no external context needed.
- **Bad fit**: anything requiring domain-rule branching, external context, or
  reaching into sibling containers (e.g. deciding which special tokens exist
  based on chosen factions — that's `new_game()`'s job, not `__post_init__`'s,
  since it's a genuine setup *decision*, not a mechanical derivation, and a
  caller might legitimately need to construct with an explicit value e.g. for
  `load`/tests).
- Caveat: `__post_init__`-computed fields are **not** automatically recomputed
  on the `load()` (`__new__`-bypass) path — `init_from_save_dict` must decide
  whether to trust the saved value directly or explicitly recompute for defensive
  consistency.

## 4. Resolved layer

- `Resolved[TState, TConfig]` — generic dataclass base (`state`, `config` fields),
  for the common one-State/one-Config case. Entities needing multiple Configs (or
  none) use a bespoke dataclass instead of forcing the generic shape.
- **Build a `Resolved*` type only once 2+ real methods genuinely need State+Config
  together** — don't build speculatively just because a State object has a
  `config_id`. (`ResolvedUnit` was justified immediately — movement, combat both
  need it. `ResolvedPlayer` was deliberately deferred until a real need — e.g.
  special-token lookup — surfaced.)
- **Never cache/store `Resolved*` objects on `GameState`** — construct on demand,
  once per operation, thread through that operation's call chain (parameters to
  sub-methods). Avoids staleness; cost of re-resolving (O(1) dict lookups) is
  negligible.
- Trait mixins at this layer are `Protocol`s (no data of their own — just forward
  to `self.state`/`self.config`), composed per concrete `Resolved*` class to match
  exactly which Config-layer traits that entity's Config type has (mirrors the
  Config-layer mixin composition 1:1).
- Config-dependent **decisions** belong at this layer (or Services), not in State:
  e.g. `Exhaustable` legality (`config.exhaustable: bool`, since it varies per
  specific card, not per class) is checked in the Resolved-layer `exhaust()`
  method before forwarding to the State mutation.

## 5. Domain Services

- For genuinely **heterogeneous, cross-entity** rules logic (`MovementService`,
  `CombatService`) — composes multiple `Resolved*` objects, not just one.
- Built on top of `Resolved*` objects, not raw State + manual `config_id` lookups
  — eliminates repeated `ruleset_config.unit(state.config_id)` boilerplate at
  every call site.

## 6. State-to-state relationship rules ("derive, don't store both sides")

Pick exactly **one side** to store a reference on — never both, never store a
computed reverse-list that could drift out of sync. Classify by cardinality:

1. **1:many** → store the "1" reference on each of the "many" (e.g. `system_id`
   on `UnitState`, not a `unit_ids` list on `SystemState`).
2. **1:many, optional on the many side** → same as (1), just `Optional`
   (e.g. `SecretObjectiveCardState.owner_player_id: str | None`).
3. **1:optional(0-1)** → store on the consistent/always-present side
   (e.g. `PlayerState.faction_config_id`, not a back-reference on `FactionConfig`).
4. **many:many** → store on whichever side "cares" about the relationship
   (e.g. `PlayerState.scored_objective_ids` — players care what they've scored;
   objectives don't care who scored them).
5. **optional:optional** → same judgment as (4): store on the side whose value
   changes / that "cares" more (e.g. Valefar Assimilator token references its
   current technology, not the reverse — the token's placement changes and is
   permanent once set; the technology doesn't change based on assimilation).

The "many" queries are **derived on demand** via filter methods on `GameState`
(e.g. `GameState.secret_objectives_held_by(player_id)`), never stored as a
separate synced list. Counts (e.g. "max 3 secret objectives") are derived the
same way, never stored as an incrementable counter.

### Worked example: Secret Objectives

- Lifecycle modeled via a `SecretObjectiveZone` enum (`DECK`, `HAND`, `SCORED`,
  `REVEALED`) on the card — not separate booleans (avoids representable-but-invalid
  states like `scored=True, owner=None`).
- `owner_player_id: str | None` on the card (rule 2) — who drew/originally scored
  it; permanent once set, independent of the `zone` transitions.
- Once a card enters `REVEALED` (via the one agenda card effect), it does **not**
  move to a different container/deck — `zone` transitions in place; "currently
  public" is a derived filter (`zone == REVEALED`), never a physical relocation.
- Scoring (who has scored what) is **unified** across Public + Secret + Revealed
  objectives into one `PlayerState.scored_objective_ids: list[str]` (many:many,
  rule 4) — enabled because both card types share one global ID space. Type
  discrimination (is this scored ID a secret objective?) is resolved via
  `RulesetConfig` lookup at query time, never stored redundantly.
- A shared `Revealable` **Protocol** (`revealed: bool` property, `reveal()` method)
  unifies `PublicObjectiveCardState` (simple stored bool) and
  `SecretObjectiveCardState` (derived from `zone == REVEALED`) under one interface
  — each concrete class keeps exactly one source of truth internally; the Protocol
  only unifies the *external* query interface.

### Worked example: Faction-dependent special tokens (Naalu, Nekro, Creuss)

- These entities' **existence itself** (not just a trait) is conditional on setup
  choices (which factions were picked) — structurally analogous to
  `UnitState`/`PlanetState`/objective cards (`GameState` only ever models what's
  *actually present* in this game, never the full space of what's *possible* —
  that's `RulesetConfig`'s job).
- Construction belongs in `new_game()` composition logic (e.g.
  `SpecialTokenStates.new_game(player_faction_ids, ruleset_config)`), **not**
  `__post_init__` (that would be reaching into external context/decisions, not
  deriving from already-provided fields) and **not** pushed to a layer above
  `GameState` (this is the same category of work `GameState.new_game()` already
  does for map layout, factions, etc.).
- Token → owner is rule 1/2 shape: `owner_player_id` stored on the token (often
  non-optional, since these tokens are only ever constructed once an owner is
  already known — no "exists but unowned" state is representable).
