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
effectively private.

**Correction — the `resolved_*()` factories live in `resolved/`, not on
`GameState` itself.** An earlier draft of this doc put `resolved_unit()`-style
factory methods directly on `GameState`. That's backwards: `state/` is not
allowed to import from `resolved/` (dependency direction is strictly
`resolved → state`, never the reverse — see above), and a method like
`GameState.resolved_unit()` would require exactly that import, creating a
circular dependency between the two modules. The fix: a `GameStateResolver`
object lives in `resolved/`, holds a `GameState` + `RulesetConfig` reference,
and is the thing that constructs `Resolved*` objects on demand:

```python
# resolved/game_state_resolver.py
class GameStateResolver:
    def __init__(self, game_state: GameState, ruleset_config: RulesetConfig):
        self.game_state = game_state
        self.ruleset_config = ruleset_config

    def resolved_unit(self, unit_id: str) -> ResolvedUnit:
        state = self.game_state.units[unit_id]
        config = self.ruleset_config.unit(state.config_id)
        return ResolvedUnit(state, config)
```

Services and the orchestrator hold/use a `GameStateResolver`, never a raw
`GameState` — that's the actual sanctioned access point. `GameState.units`/etc.
remain accessible *to `resolved/` code* (that's the normal, sanctioned
downward reach), just not constructed-from *inside* `state/` itself. This
doesn't reopen the "never cache `Resolved*` objects" rule (§4) — a
`GameStateResolver` instance is fine to hold for a whole session, since it only
holds stable references (`game_state`, `ruleset_config`) and still constructs
a fresh `Resolved*` binding on every call; nothing about the bound pair itself
is cached.

### Setup vs. play: `GameState` is constructed atomically, never incrementally

`GameState.new_game(game_setup)` is called **exactly once**,
with a complete, already-finalized `GameSetup` — never built up field-by-field
as player choices trickle in. This follows from decisions already made
elsewhere in this doc: every `new_game()` classmethod takes required,
concrete parameters (no placeholder/`None`-until-later fields), and
`__post_init__`-derived invariants (e.g. `command_token_reinforcement_pool`,
conditional special-token existence) assume complete, valid input from the
first moment the object exists. A partially-populated `GameState` would
either violate those invariants or force them to tolerate incompleteness —
degrading a guarantee that's deliberately load-bearing elsewhere.

**`GameState.new_game` takes only `GameSetup`, not `RulesetConfig`.** Verified
against the actual `GameState` class: it holds no `ruleset_config` field, and
per Principle IV (Config Immutability / State Mutability), no State class
holds a direct Config reference anywhere. Construction only ever consumes
already-*decided* identifiers (`faction_config_id`, `map_layout_id`) — it
never needs to *resolve* what those identifiers mean; that's exclusively the
Resolved layer's job, via `GameStateResolver` (below), which is why
`RulesetConfig` lives there instead. If a bootstrap layer wants to validate a
`GameSetup`'s IDs actually exist in the ruleset before constructing
`GameState`, that check belongs in the bootstrap layer itself, against
`RulesetConfig`, *before* calling `new_game` — not inside `new_game`.


The messy, in-progress part of setup (players still joining, still picking
factions/colors/drafting systems) lives entirely **outside** the State model,
in a separate, deliberately-partial structure that never pretends to be valid
`Serializable` game state:

```python
@dataclass
class GameSetupSession:
    player_faction_ids: dict[str, str] = field(default_factory=dict)
    drafted_system_ids: dict[str, list[str]] = field(default_factory=dict)
    map_layout_id: str | None = None   # genuinely "unknown so far" here — the
                                         # right place for that ambiguity to live

    def is_complete(self) -> bool: ...

    def finalize(self) -> GameSetup:
        if not self.is_complete():
            raise ValueError("setup incomplete")
        return GameSetup(player_faction_ids=self.player_faction_ids, ...)
```

Only `GameSetupSession.finalize()` succeeding produces a real `GameSetup`, and
only then does `GameState.new_game(...)` get called — once, by a
bootstrap/setup layer sitting above everything else (not Config, State,
Resolved, Services, or the gameplay Orchestrator — a distinct pre-game setup
process), producing a fully-valid `GameState` from its very first instant.

### `setup/` — a dedicated layer for pre-game data, distinct from `state/`, `resolved/`, and everything else

Lives as its own top-level package, sibling to `config/`/`state/`/`resolved/`,
in the dependency chain `config/` (+ `geometry/`) → `setup/` → `state/` →
`resolved/` → `services/` → `orchestration/`. Not `resolved/` (nothing here
binds State+Config for gameplay queries — this is pure construction input,
before any State exists at all). Not `state/` (`GameSetupSession` is
deliberately incomplete/mutable and never `Serializable`; even the finalized
`GameSetup` has no business living alongside classes that carry State's
save/load/`new_game` invariants).

**Per-entity setup data gets its own small, explicit DTO once it has 2+
related fields that travel together** (`NewGamePlayerInit`: `player_id`,
`color`, `faction_config_id`, `name`) — the alternative, N parallel dicts all
independently keyed by the same ID (`player_colors: dict[str, PlayerColor]`,
`player_faction_ids: dict[str, str]`, ...), is the same "one entity split
across containers" anti-pattern the derive-don't-store rules (§6) exist to
prevent, just recurring at setup time. A setup value that's genuinely just
one value per key (e.g. `system_id → HexCoordinate` placements) doesn't need
a wrapper DTO — a plain `MappingProxyType` already says everything there is
to say; reach for a DTO when there's a *record*, not for every mapping.

**`GameSetupSession`'s mutable containers don't need a mutable mirror of
every immutable DTO used in the finalized `GameSetup`.** Same reasoning as
the YAML loader building typed `Config` objects from raw dicts: transient,
in-progress data doesn't need type safety, because it gets validated and
typed exactly once, at a single boundary (`finalize()`). A plain
`dict[str, dict[str, ...]]`, or a `TypedDict` for a little static-checking
without any runtime class overhead, is the right shape for the session —
building `MutableNewGamePlayerInit` alongside `NewGamePlayerInit` would mean
keeping *three* things in sync (mutable version, immutable version, whatever
consumes the immutable one) instead of two. One exception: value types that
are cheap, immutable, and already shared vocabulary (`HexCoordinate`) should
still be constructed for real the moment the raw decision is captured, not
deferred as raw ints until `finalize()` — same "loader owns full nested
conversion" principle from §2, just relocated to whatever code captures a
setup decision instead of a YAML loader.

**Setup *mode* is a discriminated split, not optional fields on one shape —
worked example: First-Game vs. Complete Setup.** The rulebook's simplified
First-Game Setup (preset map by player count, a restricted 6-faction pool, no
promissory notes) and the full Complete Setup (drafted system-tile
placement, full faction roster, promissory notes included) aren't
independent toggles — they always travel together as one of two coherent
modes, so mixing traits from each (preset map + promissory notes, say) isn't
a valid game state. Same principle as Config's mutually-exclusive trait
splits (§2's `tech_type`/Assimilator example) applied to `setup/`:

```python
@dataclass(frozen=True, kw_only=True)
class FirstGameSetup:
    players: tuple[NewGamePlayerInit, ...]   # seating order, clockwise from speaker
    speaker_player_id: str
    map_layout_id: str   # preset diagram by player count

@dataclass(frozen=True, kw_only=True)
class CompleteGameSetup:
    players: tuple[NewGamePlayerInit, ...]
    speaker_player_id: str
    system_placements: MappingProxyType[str, HexCoordinate]   # drafted tiles

GameSetup = FirstGameSetup | CompleteGameSetup
```

`GameState.new_game()` pattern-matches on which variant it received to decide
**whether** a construction step runs at all — not to fill in different data.
E.g. promissory notes (*"four that match their player color, and one
faction-specific"*) need no dedicated Init field in either mode — they're
fully derivable from `NewGamePlayerInit.color`/`.faction_config_id`, data
already identical across both variants. The only thing that varies between
modes is whether `GameState.new_game()` runs that construction step at all;
mode governs *behavior*, not *data shape*. The restricted First-Game faction
pool is a `GameSetupSession`-level (lobby/UI) constraint on what gets
*offered* — never a field anywhere in the finalized `GameSetup` or beyond;
downstream code only ever sees a valid `faction_config_id` and has no reason
to know which pool it was drawn from.

**Most of a rulebook's numbered setup steps turn out not to need Init data at
all** — worked example: Twilight Imperium's 12-step First-Game Setup. Walking
through each step against the "is this a genuine per-game decision, or a
fixed/derivable default" test (same test as §3's `__post_init__` dividing
line, applied to setup instead of construction) leaves only 3 of 12 steps
producing real setup data (speaker, per-player faction+color, map). Everything
else — component counts, starting units/tech (derivable from
`faction_config_id` via `RulesetConfig`), deck contents (every matching
Config entry), pool sizes, VP-track start, objective draws — is either a
universal constant belonging in the relevant `StateObj.new_game()` default,
or randomness resolved at construction time, never setup data to capture.
When adapting a rulebook's setup procedure into Init objects, expect most
steps to collapse this way — resist the instinct to give every numbered step
its own field or DTO.

**`SetupConfig` (and `MapConfig`) live separately from `RulesetConfig`, not
as fields on it — worked example.** `RulesetConfig` is held by
`GameStateResolver` for the *entire game*, resolving `config_id → Config` on
every gameplay query, repeatedly, for the game's whole duration.
`SetupConfig` (home coordinates, advanced-setup tile counts per player
count) and `MapConfig` (map shapes) have a categorically different
lifetime — consumed only during `new_game()`/`GameSetupSession`, never again
once `GameState.systems` exists with each `SystemState.map_hex_coordinate`
baked in directly. Bundling them into `RulesetConfig` costs nothing
functionally, but misrepresents their lifetime and means every
`GameStateResolver` (and everything holding one) carries data it will never
use again after setup completes.

```python
@dataclass(frozen=True, kw_only=True)
class SetupConfig:
    map_shape_id: MapShape
    player_setup: tuple[PlayerSetupConfig, ...]
    maps: MappingProxyType[str, MapConfig]              # moved from RulesetConfig.maps
    advanced_tile_counts: MappingProxyType[int, int]     # player_count -> tiles dealt

    @classmethod
    def load(cls, config_dir: Path) -> "SetupConfig": ...
```

**This produces a clean symmetry worth stating as a general rule**, not just
a one-off fix: whether an object needs a Config reference at all follows
from whether it's a **one-shot construction** or an **ongoing/resolving
process**, not from which layer it happens to sit in.

| | Construction-only (no Config needed) | Ongoing/resolving (holds Config) |
|---|---|---|
| Gameplay | `GameState` — consumes already-decided IDs once, at `new_game()` | `GameStateResolver` — resolves `config_id → Config` repeatedly, for the whole game |
| Setup | `GameSetup` — the finalized, immutable output; never resolves anything itself | `GameSetupSession` — interactive; needs `SetupConfig` repeatedly as players join, colors are picked, tiles are dealt |

`GameSetupSession` holds `setup_config: SetupConfig` for its whole
interactive lifetime, exactly as `GameStateResolver` holds `ruleset_config`
— both are the "ongoing" half of their respective pair. `GameState` and
`GameSetup` are both the "one-shot" half, and neither holds Config, for the
same underlying reason.

**Setup phases: one enum-gated session class, not a `Phase1`/`Phase2` class
split — worked example.** Some setup data has a real *dependency order* (the
player count must be confirmed before advanced-setup tile counts can be
looked up), which might suggest splitting `GameSetupSession` into separate
classes per phase. Don't — this is the same "not yet complete" shape
`GameSetupSession` already has, just with an intermediate checkpoint added,
not a fundamentally different terminal shape the way
`FirstGameSetup`/`CompleteGameSetup` genuinely are (§1). A `StrEnum` phase
gate on the *same* session class, mirroring `SecretObjectiveZone`'s
"illegal combinations should be unrepresentable" principle (§6) applied to
setup instead of gameplay state:

```python
class SetupPhase(StrEnum):
    JOINING = "joining"                 # players adding/removing, names, colors
    ROSTER_LOCKED = "roster_locked"      # player count confirmed — setup lookups now resolvable

@dataclass
class GameSetupSession:
    setup_config: SetupConfig
    players: dict[str, PlayerSetupDraft] = field(default_factory=dict)
    phase: SetupPhase = SetupPhase.JOINING

    def add_player(self, player_id: str, name: str) -> None:
        if self.phase != SetupPhase.JOINING:
            raise InvalidSetupTransition("roster is locked")
        self.players[player_id] = {"name": name}

    def confirm_roster(self) -> None:
        if self.phase != SetupPhase.JOINING:
            raise InvalidSetupTransition("roster already locked")
        if not (3 <= len(self.players) <= 6):
            raise ValueError(f"invalid player count: {len(self.players)}")
        self.phase = SetupPhase.ROSTER_LOCKED

    @property
    def player_setup_config(self) -> PlayerSetupConfig:
        if self.phase == SetupPhase.JOINING:
            raise InvalidSetupTransition("roster not yet locked")
        return self.setup_config.player_setup[len(self.players)]
```

**No separate `confirmed_player_count: int` field** — that would be the same
redundant-storage pattern §6 exists to prevent, just recurring at setup time.
Once `phase >= ROSTER_LOCKED`, mutation methods are guarded against further
changes to `players`, so `len(self.players)` stays reliable on its own;
there's nothing to store that isn't already derivable, and the phase gate is
precisely what makes that derivation *safe* to rely on (the count can't
silently change out from under a caller after being read).

### Who owns what, and why — the dividing lines

The boundaries between layers get murky in the moment (mid-design, a field or
a method can plausibly "belong" in more than one place). This table is the
condensed answer arrived at, layer by layer, plus the one-line test that
settles the murky cases.

| Layer | Owns | Never owns | One-line test |
|---|---|---|---|
| `data/` (YAML) | Raw static content, nothing else | Any typed shape, any logic | — |
| `config/` | The complete, final **typed** shape of static ruleset data; **all** conversion from raw YAML into that shape, including nested/composed value types (§2) | Anything per-game or live; any decision that depends on which game is being played | "Is this true independent of any specific game being played?" → Config. "Only true in the context of one ongoing match?" → State. |
| `state/` | Live, mutable, per-game data; identity (`instance_id`); self-contained mutation taking **primitives**, never Config objects; references to Config/other State **by id only** (§6 derive-don't-store rules) | Config *values* (only `config_id`); decisions requiring Config; cross-entity coordination; setup decisions requiring external context (that's `new_game()`'s job, not the class's fields/shape) | "Does this field/method need only this object's own already-known data?" → State. "Does it need to look up or reason about Config content?" → not State. |
| `resolved/` | Binding one live State + its resolved Config, for the duration of one operation; single-entity Config-aware queries/decisions; `GameStateResolver` is the sanctioned entry point for constructing `Resolved*` objects (holds `GameState` + `RulesetConfig`) | Storage (never persisted — §4); cross-entity coordination | "Does answering this need only *this one entity's* State + Config?" → Resolved. "Needs another entity too?" → Service. |
| `services/` | Cross-entity rules logic; decisions composing multiple `Resolved*` objects | Sequencing/turn order; raw State/Config manipulation (delegates down to Resolved/State) | "Does this require reasoning about 2+ entities together?" → Service. |
| `orchestration/` | Sequencing/flow: *when* an operation fires, in response to what trigger, during what phase | The rule mechanics themselves (what's legal, what happens) — those live in Services/Resolved | "Is this deciding *whether/when* to call a rule, or *being* the rule?" — deciding when → orchestration; being the rule → Service/Resolved. |
| `geometry/` | Pure hex-coordinate math, zero game-concept awareness | Any assumption that a caller knows about game rules | — |

Construction-specific dividing line (§3 has the full version): *"Is this
value invariant across every possible way the object gets built?"* → belongs
in `__post_init__`. *"Does it vary depending on which classmethod
(`new_game`/`load`) is doing the constructing?"* → belongs in that
classmethod, not `__post_init__`.

## 2. Config layer

- `RulesetConfig` is the static-data aggregate: loaded once (`RulesetConfig.load(config_dir)`),
  shared across every concurrent `GameState`, independent of any specific game
  (independent of player count, factions chosen, etc.). Frozen/immutable.
- Per-type loader functions (`load_strategy_card_data`, etc.) live in
  `config/yaml_loader.py`, each returning **already-typed Config objects**
  (never raw dicts) — loaders own "YAML shape → typed object," `RulesetConfig.load`
  only composes the results.
- **The loader owns *all* nested/composed type conversion, not just the outer
  object.** E.g. `MapConfig.tiles: tuple[HexCoordinate, ...]` — the loader
  builds fully-formed `HexCoordinate` instances from the raw `list[list[int]]`
  YAML shape itself; `MapConfig`'s constructor only ever receives already-typed
  `HexCoordinate` objects, never raw ints/lists it would need to coerce itself.
  Splitting this (loader builds the outer container, the Config class coerces
  the inner values) would smear a single responsibility across two places and
  make the Config class harder to construct directly in tests/fixtures.
  Corollary: no generic reflection-based "auto-coerce dicts to `MappingProxyType`
  by inspecting type hints" helper — the field's declared type
  (`tuple[...]`, `MappingProxyType[...]`) already *is* the immutability
  contract on a frozen dataclass; the loader just needs to construct that type
  once, explicitly, same as everything else it builds.
- `RulesetConfig` builds `MappingProxyType` indices (ID → object) in `__post_init__`
  for O(1) lookup, alongside the ordered tuple form if needed.
- Config classes use trait mixins for optional fields (`RequiresFunctionalText`,
  `RequiresFlavorText`, `RequiresFlavorTextOptions`) — composed per card type as needed.
- Enums (`UnitClass`, `TechType`, etc.) live alongside the Config class that
  owns their vocabulary (e.g. `config/objs/unit/unit_class.py`), each
  subclassing the shared `ConfigEnum`/`SerializableEnum` bases in
  `config/shared/enum.py` — static vocabulary, imported freely by
  State/Resolved without violating layering.
- `HexCoordinate` (from `geometry/`) is imported into Config the same way — a shared
  value type, not a data-coupling.
- Naming: settled on **`RulesetConfig`**, not `GameConfig` — signals "static ruleset,"
  not "belongs to one game."
- **`slots=True` is not used on Config (or State) dataclasses.** Verified: combining
  two `slots=True` trait mixins via multiple inheritance raises
  `TypeError: multiple bases have instance lay-out conflicts`. Slotting only the
  leaf class while mixins stay unslotted avoids the error but delivers **zero**
  memory benefit — the instance still gets a `__dict__` the moment *any* class in
  the MRO lacks `__slots__`. Since nearly every Config class is composed from 2+
  trait mixins, there is no configuration that both avoids the conflict and
  actually saves memory without abandoning the mixin-composition pattern.
  Measured savings would be ~288 bytes/instance if it worked at all — at a
  realistic few-thousand-instance ruleset, well under 1MB total. Not worth
  restructuring around; omit `slots=True` everywhere for consistency.

### Optional-but-structural fields: subclass/trait split, not `Optional`

Use `Optional[X] = None` only when `None` means "legitimately unknown/unset,
but the field's concept still applies to this instance." When a field's
*concept itself* doesn't apply to some subset of instances (not "unknown
value," but "this question doesn't make sense here"), that's a signal for a
trait split (matching the `RequiresFlavorText`/`RequiresFlavorTextOptions`
pattern), not a nullable field — otherwise you get an illegal state that's
*representable* (`None` where it shouldn't be) and can only be caught by a
test enforcing "everything except these N special cases has a value," rather
than being structurally impossible to construct wrong.

**Worked example: Technology `tech_type`.** Every technology has a static
`TechType` (biotic/propulsion/cybernetic/warfare) — except the two Valefar
Assimilator technologies, which have no fixed type at all; they take on
whichever type the technology they're placed on has. Modeled as:

```python
@dataclass(frozen=True, kw_only=True)
class TechConfig(NamedConfigObj, RequiresFunctionalText, CanHaveFactionExclusivity, CanBeExhaustible):
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()
    # no tech_type field here — not universal

@dataclass(frozen=True, kw_only=True)
class StandardTechConfig(TechConfig):
    tech_type: TechType   # required, not nullable

@dataclass(frozen=True, kw_only=True)
class AssimilatorTechConfig(TechConfig):
    pass   # structurally has no tech_type — matches the domain truth exactly
```

`load_tech_data` picks the subclass per YAML entry — by id, checking against
the two known `TechID.VALEFAR_ASSIMILATOR_X`/`_Y` values in
`config/objs/tech/ids.py` (a `discriminator id → subclass` check, not by
checking whether `tech_type` happens to be null). The *live, current* type of
an in-play Assimilator (derived from whichever tech State it's currently
placed on — see §6 rule 5, Valefar Assimilator token) is a Resolved-layer
concern, not Config — `AssimilatorTechConfig` correctly has no field for it
at all. A `HasCurrentTechType`-style Resolved Protocol could unify that query
(`current_tech_type`) across both subclasses once the Resolved layer reaches
Tech, each resolving it differently underneath — same shape as `Revealable`
in §6. (Not built yet — Resolved-layer Tech support doesn't exist yet.)

**Refinement — scale and existing discriminators matter, not just whether
`None` is ambiguous in the abstract.** The subclass-split answer above is
right for `tech_type` (2 exceptions out of ~90, no existing discriminator to
lean on). It is **not** automatically right for every optional-but-structural
field — weigh it against how many instances are affected, and whether a
discriminator already exists elsewhere that every caller is already required
to check.

**Worked example: Agenda `target_id`.** Of 50 Agenda cards, ~9 attach to a
planet and ~13 attach to a player (mutually exclusive — a card is always
exactly one `AgendaVoteType`: `FOR_AGAINST`, `ELECT_PLAYER`, `ELECT_PLANET`,
`ELECT_LAW`, `ELECT_SCORE_SECRET_OBJECTIVE`). Splitting into subclasses here
would mean 22/50 cards moving to specialized types, real `yaml_loader`/
`save`/`new_game` complexity across ~5 shapes, to guard against an ambiguity
that's already resolved by a field Config *already has*:

```python
@dataclass(frozen=True, kw_only=True)
class AgendaConfig(NamedConfigObj, CanBeExhaustible):
    vote_type: AgendaVoteType
```

```python
@dataclass(kw_only=True)
class AgendaCardState(ExhaustableStateMixin):
    target_id: str | None = None   # elected player_id or planet_id — meaning
                                     # determined by Config's vote_type, never
                                     # read without checking it first
```

Every `instance_id` in the whole State model is a globally-unique `uuid4()`,
so one field can safely hold "whichever kind of entity `vote_type` says this
card elects" — same trick that let `PlayerState.scored_objective_ids` unify
Public/Secret objective IDs (§6). `target_id` is only ever read after checking
`ruleset_config.agenda(card.config_id).vote_type` — same Config-gated access
discipline already used for `exhaustable` legality, extended to a second field.
**Rule of thumb:** reach for a subclass split when the field is rare (small
fraction of instances) *and* there's no existing enum every caller already
checks; reach for a flat nullable field, gated by an existing discriminator,
when neither condition holds.

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
- **`slots=True` is not used on State dataclasses** — same rationale as
  Config (§2): combining 2+ `slots=True` trait mixins via multiple
  inheritance raises `TypeError: multiple bases have instance lay-out
  conflict`, and slotting only the leaf class while its mixins stay unslotted
  still gets a `__dict__` from the first unslotted class in the MRO,
  delivering zero memory benefit. State's mixin composition
  (`ConfigIDStateObj`/`UUIDInstancedStateObj`, `Exhaustible`,
  `PlayerOwnableMixin`, etc.) hits the identical conflict; omit `slots=True`
  everywhere in `state/` for the same reason.
- **`frozen=True` is not used on State dataclasses** — structurally
  incompatible with `Serializable.load()`'s `cls.__new__(cls)` + mutate
  pattern: a frozen dataclass overrides `__setattr__` to always raise
  `FrozenInstanceError`, regardless of the `__new__` bypass used to
  construct the instance, and Python additionally requires `frozen` to
  match consistently up a dataclass inheritance chain — a `frozen=True`
  leaf can't inherit from a non-frozen shared base like `ConfigIDStateObj`
  or `Serializable` without one or the other giving way. Every State class
  must support the `load()` path, so none may be `frozen=True`. Fields that
  are conceptually immutable after construction (e.g.
  `SystemState.map_hex_coordinate`, `PromissoryNoteCardState`'s issuing
  color) are typed `Final[...]` instead — a static/convention-level
  contract, not a dataclass-enforced one — matching the pattern already
  used for `PlayerState.color`/`name`/`faction_id`.

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

**Worked example: `exhausted` must never be `bool | None`.** Only some Tech
(and some Agenda) cards are exhaustible — the temptation is to make the State
field `bool | None` to represent "doesn't apply." Don't: `exhausted=False` is
never ambiguous, even for a card that can *never* be exhausted — it's simply,
harmlessly true ("not currently exhausted"). The "is this exhaustible at all"
fact belongs on **Config**, not State: `TechConfig` already composes
`CanBeExhaustible` (per §2) for exactly this reason, and `AgendaConfig` should
too. Every `TechCardState`/`AgendaCardState` composes `ExhaustableStateMixin`
**unconditionally**, with a plain `exhausted: bool = False` — no `Optional`,
no per-card conditional field, no subclass split. Legality (can this specific
card actually be exhausted) is checked once, at the Resolved-layer `exhaust()`
method, against `config.exhaustable`/the `CanBeExhaustible` mixin data —
never by inspecting whether the State field happens to be `None`. This is the
simplest point on the same spectrum as the `tech_type` and `target_id`
examples above: a plain unconditional field, gated by Config, needs neither
`Optional` nor a subclass — reach for those only when the field's *meaning*
(not just its legality) genuinely varies per instance.

### `Serializable` — single shared terminal / ABC root

- All per-field "cooperative super() chains" (save/load) terminate at one shared
  `Serializable`, not multiple competing terminal classes. Consolidating into one
  avoids silently-incomplete chains (a mixin's `super()` call reaching an
  unintended, differently-scoped terminal).
- `Serializable` implements the save/load contract concretely (`save`,
  `init_from_save`) — as **`ABC` + `@abstractmethod`**, not `Protocol`, since
  every State-layer class already shares this one common ancestor (real
  inheritance tree, not cross-hierarchy structural typing). Both abstract
  methods still carry a real no-op terminal body (`save` returns `{}`;
  `init_from_save` is a no-op `pass`) rather than `...` — every leaf's
  `super().save() | {...}` chain needs an actual `dict` to merge into at the
  top (`None | {...}` raises `TypeError`); `@abstractmethod` alone still
  forces every concrete class to provide its own override.
- **`Loadable` was retired** — its one implementation (`load`: `cls.__new__(cls)`
  + `obj.init_from_save(data)`) never varies per class, so it's just a plain
  concrete `classmethod` on `Serializable`, not a separate Protocol.
- `save`/`init_from_save` **do** stay as genuinely overridden,
  cooperative (`super()`-chained) methods — each trait mixin and leaf class
  contributes its own slice, chaining up through `Serializable`'s no-op
  terminal. This is real per-class variation, unlike `load`. `__post_init__`
  is *not* part of this cooperative chain today — `Serializable` has no
  `__post_init__` of its own, so leaf classes must not call
  `super().__post_init__()` unless/until a shared base actually defines one.

### `new_game` vs. `load` — different problems, different mechanisms

- **`load(data: dict)`**: needs `cls.__new__(cls)` (bypasses `__init__` entirely)
  because it receives an **opaque nested dict** that must be unpacked/reconstructed
  per-field — cooperative `init_from_save` chaining is real, necessary work here.
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
  on the `load()` (`__new__`-bypass) path — `init_from_save` must decide
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
