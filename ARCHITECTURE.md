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
layers never import from higher ones. `geometry` and `config/enum.py`
(`ConfigEnum`/`SerializableEnum`) are shared vocabulary/types that any layer
may import — that's importing a *type*, not coupling to *data*, so it doesn't
violate the boundary.

**The orchestrator never touches raw `GameState` containers directly.** It only
calls `Resolved*` objects and Domain Services. `GameState`'s containers are
effectively private; `GameStateResolver` (`resolved/game_state_resolver.py`,
constructed from one `GameState` + one `RulesetConfig`) is the only
sanctioned way to turn an id into a `Resolved*` object, via its
`resolved_player`/`resolved_unit`/`resolved_planet`/`resolved_system`
methods. `Domain Services` (§5) hold a `GameStateResolver` and call through
it rather than touching `GameState`/`RulesetConfig` directly.

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
| `resolved/` | Binding one live State + its resolved Config, for the duration of one operation; single-entity Config-aware queries/decisions | Storage (never persisted — §4); cross-entity coordination | "Does answering this need only *this one entity's* State + Config?" → Resolved. "Needs another entity too?" → Service. |
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
- **Loaders are colocated per-entity functions, not a monolithic module and not
  a Loader class hierarchy.** Each entity owns its own parsing, living next to the
  Config class it builds: `config/objs/unit/loader.py` holds `load_unit_data(root)`
  (and its private `_parse_unit`), beside `UnitConfig` and its enums — the whole
  "what is a unit / how is one built from YAML" story in one folder. This
  supersedes the earlier monolithic `config/yaml_loader.py`, which had become a
  dumping ground coupling every entity's parsing into one file. Each `load_X_data`
  returns **already-typed Config objects** (never raw dicts); `RulesetConfig.load`
  stays a composition root that imports each `load_X_data` from its entity module
  and assembles the results.
- **Share the YAML *mechanism* by function call, not inheritance.** A base
  `Loader` class whose `load()` is inherited by `UnitLoader`/`TechLoader`/... is
  the wrong tool — it proliferates one-method classes that share no state and
  exercise no polymorphism (a "class where a function would do"), and a base
  class exerts gravitational pull that scatters loaders into a shared package,
  fighting the colocation goal above. Instead, separate the two concerns as
  layered functions: shared low-level `load_data(path) -> Any` / `load_folder_data(dir) -> list[Any]`
  (file(s) → raw dict/list, identical for everyone, in `config/yaml_loader.py`,
  along with the shared `CONFIG_OBJ_DATA_PATH`/`SETUP_CONFIG_DATA_PATH` path
  constants), which each colocated `load_X_data` **back-calls** for the I/O
  step before doing its own entity-specific dict→Config parsing. "File → raw
  structure" is shared and called; "raw structure → typed X" is unique and
  colocated. Same for the common text-merge step: `merge_text_by_id(config_dicts,
  text_dicts)` is a shared **pure** function (no `Path`, no I/O — so it's
  testable with in-memory dicts) in `config/objs/text_merge.py`, alongside the
  convenience `load_and_merge_text_by_id(root_path, rel_path)` that composes it
  with the load step for the common single-file case; composed by the
  text-bearing entities' loaders.
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
- **Root path injection stays; per-entity loaders hardcode their own relative
  filename.** `load_X_data(root)` takes the data root as a parameter (the one
  thing tests need to vary — point at a fixture tree), and combines it with a
  hardcoded relative filename/subdir internally. Filenames aren't parameters —
  a loader's coupling to its one file is fixed and permanent, so parameterizing
  it buys no testability, just call-site noise. Keep shared path constants
  private/relative; never promote the file layout into the caller's contract.
- Every `load_X_data` returns its `MappingProxyType[str, X]` (ID → object)
  index directly, built via the shared `index_by_id(configs)` helper
  (`config/objs/index.py` — raises `DuplicateConfigIDError` rather than
  letting a later entry silently clobber an earlier one with the same id).
  `RulesetConfig.load` is a pure aggregation of already-indexed mappings, so
  `RulesetConfig` itself needs no `__post_init__` to build indices — the
  per-entity loader is a more specific place to catch a duplicate id than a
  single index-everything step on the aggregate.
- **`FromDictMixin`** (`config/fromdict.py`) is the shared dict→instance
  coercion contract: `from_dict(data)` copies the incoming dict (never
  mutates the caller's — matters for YAML anchors/aliases resolving to the
  *same* dict object), calls the subclass's `_init_from_dict(d)` to coerce
  any nested/composed fields in place, then constructs `cls(**data)`. Only
  compose it on a class that actually *has* a field needing coercion (a
  nested Config type, an enum, a tuple built from a raw list); a class whose
  fields are all already YAML-native primitives doesn't need it and doesn't
  get a `from_dict` at all (e.g. `AssimilatorTechConfig` — see the Tech
  worked example below).
- Config classes use trait mixins for optional fields (`RequiresFunctionalText`,
  `RequiresFlavorText`, `RequiresFlavorTextOptions`) — composed per card type as needed.
- Enums (`UnitClass`, `TechType`, etc.) live alongside the Config class that
  owns their vocabulary (e.g. `config/objs/unit/unit_class.py`), each
  subclassing the shared `ConfigEnum`/`SerializableEnum` bases in
  `config/enum.py` — static vocabulary, imported freely by
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
class TechConfig(NamedConfigObj, RequiresFunctionalText):
    # no tech_type field here — not universal
    # no prereqs field here either — see below
    # no faction-exclusivity mixin here either — see below
    # no CanBeExhaustible here either — see below
    pass

@dataclass(frozen=True, kw_only=True)
class StandardTechConfig(TechConfig, CanHaveFactionExclusivity, CanBeExhaustible, FromDictMixin):
    tech_type: TechType   # required, not nullable
    prereqs: tuple[TechUpgradeReqConfig, ...] = ()

@dataclass(frozen=True, kw_only=True)
class AssimilatorTechConfig(TechConfig, RequiresFactionExclusivity):
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

**Faction exclusivity on Tech is a second, independent split on the same two
subclasses — different cardinality, not different existence.** Most standard
techs aren't faction-locked, but some are (e.g. faction-specific upgrades),
so `StandardTechConfig` composes `CanHaveFactionExclusivity`
(`faction_exclusive_id: str | None = None`). The two Valefar Assimilator
tokens, by contrast, are *only ever* printed for Nekro Virus — there's no
real case where one exists without a faction — so `AssimilatorTechConfig`
composes `RequiresFactionExclusivity` (`faction_exclusive_id: str`, no
default) instead. `TechConfig` itself carries neither mixin: putting
`CanHaveFactionExclusivity` on the shared base and simply re-declaring
`faction_exclusive_id: str` on `AssimilatorTechConfig` does *not* work — a
dataclass subclass that re-annotates an inherited field without assigning a
new value still inherits the base's default via normal attribute lookup
(verified: `B(A)` re-declaring `x: str` over `A`'s `x: str = None` still
constructs `B()` successfully with `x=None`), so the field silently stays
optional. The only reliable way to flip optional→required across a subclass
boundary is to put each cardinality's mixin on the branch that needs it, not
on the shared ancestor.

**`CanBeExhaustible` is likewise only on `StandardTechConfig`, not `TechConfig`.**
An Assimilator token isn't a real card that gets drawn and exhausted in its
own right — it's a marker that borrows whatever technology it's assimilated.
"Can this be exhausted" is a question that only makes sense for a real
in-play tech, so the mixin belongs on `StandardTechConfig` alone, following
the same rule as the tech_type/faction-exclusivity splits above: don't put a
mixin on the shared base unless *every* subclass genuinely needs it.

**`prereqs` moved to `StandardTechConfig` for the same reason — an Assimilator
token isn't "upgraded through" the tech tree, so it has no prerequisites at
all.** This has a knock-on effect on `FromDictMixin`: once `prereqs` (needing
`TechUpgradeReqConfig` coercion) and `tech_type` (needing `TechType(...)`
coercion) both live only on `StandardTechConfig`, every field remaining on
`AssimilatorTechConfig` (`id`, `name`, `functional_text`,
`faction_exclusive_id`) is already a YAML-native primitive that needs no
coercion at all. So `FromDictMixin` also moves down to `StandardTechConfig`
only — `AssimilatorTechConfig` has no `from_dict`, and `load_tech_data`
constructs it directly (`AssimilatorTechConfig(**d)`) instead. This is the
general pattern: `FromDictMixin` belongs on whichever class actually needs to
convert raw dict values into richer types, not reflexively on every Config
class — a class with only primitive fields doesn't need it.

**Contrasting example: standard vs. advanced setup config — *pairing*, not a
split and not an `Optional`.** Every player count has *both* a standard and an
advanced setup definition, always, 1:1 — neither is a specialization of the
other, and neither is ever absent. That relationship is neither the `tech_type`
case (a field whose concept is absent for a subset → subclass) nor a nullable
field (sometimes-absent → `Optional`). It's two complete, coexisting
configurations held side by side, with *which one applies* decided at runtime.
The implementation (`config/setup/base.py`, `config/setup/advanced.py`)
settled on a **flattened** version of this pairing rather than two fully
parallel sibling objects — the "standard" fields live directly on
`SetupConfig` itself, and only `advanced` is a nested sibling substructure:

```python
@dataclass(frozen=True, kw_only=True)
class AdvancedMapSetupTileConfig(FromDictMixin):
    tile_color: TileColor          # BLUE or RED only — validated in __post_init__
    num_tiles: int                 # must be >= 1 — validated in __post_init__

@dataclass(frozen=True, kw_only=True)
class AdvancedSetupConfig(FromDictMixin):
    setup_tiles_per_player: tuple[AdvancedMapSetupTileConfig, ...]
    extra_setup_tiles: tuple[AdvancedMapSetupTileConfig, ...] = ()

@dataclass(frozen=True, kw_only=True)
class PlayerSetupConfig(FromDictMixin):
    home_system_coordinates: HexCoordinate
    trade_good_bonus: int = 0

@dataclass(frozen=True, kw_only=True)
class SetupConfig(FromDictMixin):        # the per-player-count pairing
    map_shape_id: MapShape
    player_setup: tuple[PlayerSetupConfig, ...]   # "standard" fields, flattened in
    advanced: AdvancedSetupConfig                  # required, not `| None` — always present

    @property
    def num_players(self) -> int:
        return len(self.player_setup)            # derived, never stored
```

`advanced` is a **required** field, not `AdvancedSetupConfig | None`: since it's
always present, it's a plain required field, which sidesteps the null-check
ambiguity an `Optional` would introduce. There is no separate
`StandardSetupConfig` sibling class — once "standard" turned out to be just
`SetupConfig`'s own base shape (map + per-player setup), giving it its own
parallel class would have meant an empty pass-through wrapper for no benefit;
`advanced` earns its own nested class because it has multiple fields
(`setup_tiles_per_player`, `extra_setup_tiles`) that don't belong flattened
onto `SetupConfig` directly. `player_count` likewise isn't a stored field —
`num_players` is a derived `@property` off `len(player_setup)`, so it can
never drift out of sync with the actual player list (`config/setup/loader.py`'s
`load_setup_data(root, num_players)` linear-scans `setup.yaml`'s entries and
matches on this derived value). The config layer stays **mode-agnostic** — it
carries `advanced` unconditionally, whether or not a given game uses it; mode
selection (choosing to consume `.advanced` vs. the flattened standard fields)
is runtime-layer (`GameSetupSession`/`new_game`) responsibility, matching the
pattern below, though a `SetupMode`-driven dispatch isn't wired up yet —
`GameSetupSession` currently only consumes the flattened standard field
(`player_setup`). This mirrors
"mode governs behavior, not data shape." `data/setup/setup.yaml` reflects the
flattened shape directly — each per-player-count entry has `map_shape_id`/
`player_setup` at the top level and a nested `advanced:` block, with no
separate `standard:` block, since those fields already live on `SetupConfig`
itself.

**The decision family, summarized** (three relationships that look similar but
resolve differently): concept-absent-for-a-subset → subclass split
(`tech_type`); sometimes-absent-value → `Optional`; both-always-present-selected-
at-runtime → required-field pairing of siblings (setup config). Match the shape
to the actual relationship, not to surface similarity.

**Worked example: Promissory Note templated text — structural segments, not a
hard-coded placeholder string.** A standard promissory note's functional text
names the *issuing player's color* mid-sentence (e.g. "...return this card to
the Yellow player."), but that color isn't known until a specific game
assigns the card to a player — unlike a faction promissory note, whose text
is fully static. An earlier draft stored the standard note's text as one
string with a placeholder token, replaced via `str.replace()` at query time —
rejected in favor of a structural split, matching this project's general
distaste for stringly-typed workarounds for a color that's a real, typed
`PlayerColor` value:

```python
@dataclass(frozen=True, kw_only=True)
class PromissoryNoteConfig(NamedConfigObj):
    pass

@dataclass(frozen=True, kw_only=True)
class FactionPromissoryNoteConfig(PromissoryNoteConfig, RequiresFactionExclusivity, RequiresFunctionalText):
    pass    # fully static text — no player color ever appears in it

@dataclass(frozen=True, kw_only=True)
class StandardPromissoryNoteConfig(PromissoryNoteConfig, FromDictMixin):
    # The raw YAML is a list of text *segments*, split at every point the
    # issuing player's color needs to be inserted - never a single string
    # with a placeholder substring to find-and-replace.
    player_color_functional_text: tuple[str, ...]
```

`ResolvedPromissoryNote.functional_text` does the actual assembly, joining
the segments with the *live* `PlayerColor` pulled from
`PromissoryNoteCardState.issuing_player_color` (`Final[PlayerColor | None]`,
`None` until the card is issued) — this is Resolved-layer work precisely
because it needs *both* the Config (the static segments) and the State (the
live color) together, matching §4's rule for when a `Resolved*` type earns
its methods:

```python
@property
def functional_text(self) -> str:
    if isinstance(self.config, StandardPromissoryNoteConfig):
        return f" {self.state.issuing_player_color} ".join(self.config.player_color_functional_text)
    return self.config.functional_text
```

`ResolvedPromissoryNote.__post_init__` also enforces the state/config pairing
invariant this split creates: a `StandardPromissoryNoteConfig` must be paired
with a State that *has* an issuing color, and a `FactionPromissoryNoteConfig`
must be paired with a State that does *not* — raising `ValueError` if either
is violated, since those are the only two valid combinations and nothing
short of a runtime check (config subclass vs. state's optional field, two
independently-typed pieces) can make the invalid pairing structurally
unrepresentable.

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
  dataclass mixin (e.g. `PlayerOwnableMixin`, `Exhaustible`).
- **Only declares a required shape, no data of its own, used across *unrelated*
  class families with no common ancestor** (e.g. Config-layer + Resolved-layer
  traits)? → `Protocol`.
- **Every implementer already shares one common concrete ancestor, and the method
  signature is uniform?** → prefer `ABC` + `@abstractmethod` over `Protocol` — gives
  real **construction-time** enforcement (`TypeError` if unimplemented), stronger
  than `Protocol`'s call-time (`NotImplementedError`) or static-only (`mypy`) checks.

**Composition over inheritance** for mechanism-sharing mixins whose *generic verb
names* shouldn't leak onto the leaf class's public surface:
- Player ownership (`state/base/ownable.py`) is split into two layers: the
  private `_PlayerOwnable` dataclass holds the real data
  (`owned_by_player_id: str | None`) and the mechanism
  (`set_owner`/`release_owner`/`is_owned`/`is_owned_by_player`); the public
  `PlayerOwnableMixin` *composes* it as a field (`ownable: _PlayerOwnable`,
  `default_factory=_PlayerOwnable`) rather than inheriting it, because
  different leaf types use different domain vocabulary for the same
  mechanism — a Planet is "controlled" (`assign_control`), a Speaker Token is
  "assigned" (`assign_speaker`). Each leaf writes its own thin, domain-named
  forwarding method to `self.ownable.set_owner(...)`. This avoids leaking the
  generic method name onto every leaf's public API. A structural
  `OwnableEntity` Protocol (`ownable: _PlayerOwnable`, `id: str`) lets
  `BaseService._require_ownership` check ownership generically against any
  leaf type without caring which domain vocabulary that leaf exposes
  publicly.
- `Exhaustible` (`state/base/exhaustible.py`) is **inherited directly**, not
  composed, because "exhaust"/"ready" terminology never diverges across
  entity types in this game — no vocabulary to protect, so composition's
  benefit doesn't apply. Rule of thumb: compose when vocabulary varies by
  leaf type; inherit directly when it doesn't.
- An earlier draft added a `Protocol` convenience mixin (`HasOwnership`) to
  supply default forwarding methods for leaf types with no vocabulary to
  protect — **removed**: it added a second, largely-redundant inheritance
  path for a one-line forward (`self.ownable.set_owner(...)`) that a leaf
  class can just as easily write itself, or, when it has no bespoke
  vocabulary at all (e.g. `NaaluTokenState`), skip entirely and call
  `.ownable.set_owner(...)` straight through the composed field.

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
- `UUIDInstancedStateObj.instance_id` uses
  `field(init=False, default_factory=lambda: uuid4().hex)` — not a required
  no-default field, and not even settable through the constructor
  (`init=False`) — since identity is never a legitimate value for a caller to
  supply; combined with `default_factory`, this also lets trivial "no real
  setup needed" leaf classes (e.g. `NaaluTokenState`) construct via plain
  `cls()` with zero required arguments where appropriate.

### `__post_init__` — when it's appropriate

Test: *"If I explicitly pass a value for this field to the constructor, does
`__post_init__`'s logic respect it, or silently clobber it?"* — if clobber, it
doesn't belong in `__post_init__`.

- **Good fit**: purely structural derivations from already-provided sibling
  fields, with no legitimate independent value a caller could want instead.
  - **Stronger version, prefer it when possible: don't even compute-and-store
    in `__post_init__` — derive on every access via a plain `@property`
    instead**, so there's no field to keep in sync (or forget to recompute on
    `load()` — see the caveat below) and nothing to save/restore at all.
    `PlayerState.command_token_reinforcement_pool` was originally a
    `__post_init__`-computed field; it's now `@property` returning
    `16 - (tactic_pool + fleet_pool + strategy_pool)` on every access — same
    "always synchronized, pure arithmetic, no domain-rule branching" reasoning
    as before, just with nothing stored (and so nothing `save()`/`init_from_save`
    need to carry).
  - `__post_init__` is still the right tool when the derived value must be a
    real *stored* field (e.g. because something else needs to reference it by
    identity, or recomputing per-access would be wasteful) rather than a
    cheap-to-recompute property — none of the current classes need this
    today, but the tool remains available for when one does.
  - Cross-field **validation** (not derivation) is also a good fit, since it
    never clobbers an explicitly-passed value, only rejects an invalid
    combination of already-provided fields: `AgendaConfig.__post_init__`
    rejects a non-`None` `planet_trait` on any `vote_scenario_type` other than
    `ELECT_PLANET`; `AdvancedMapSetupTileConfig.__post_init__` rejects
    `num_tiles < 1` and a `tile_color` outside `{BLUE, RED}`.
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

- `BaseResolvedObj[TState: Serializable, TConfig: IDConfigObj]` (`resolved/base.py`)
  — generic `slots=True, frozen=True` dataclass base (`state`, `config` fields),
  for the common one-State/one-Config case. Entities needing multiple Configs (or
  none) use a bespoke dataclass instead of forcing the generic shape (e.g.
  `ResolvedPromissoryNote` still fits the generic shape but adds `__post_init__`
  validation on top of it — see the Promissory Note worked example in §2).
- **`GameStateResolver`** (`resolved/game_state_resolver.py`) is the single
  factory for every `Resolved*` object: constructed from one `GameState` +
  one `RulesetConfig`, its `resolved_player`/`resolved_unit`/`resolved_planet`/
  `resolved_system` methods look up the State and Config halves by id and
  wrap them. Every "unknown id" failure mode is a subclass of the shared
  `UnknownEntityError` (`GameError` → `UnknownEntityError` → e.g.
  `UnknownDeployedUnitError`, `UnknownSystemStateError`), which overrides
  only a `ClassVar[str] entity_type` label — the base `__init__` builds the
  full message from it, so a new "unknown X" error is a two-line class, not a
  hand-written message at every call site. `GameStateResolver._get` is the
  shared lookup helper (`dict[id] → value`, or raise the given error class)
  that every `resolved_*` method calls.
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
  e.g. `Exhaustible` legality (`config.exhaustible: bool`, since it varies per
  specific card, not per class) should be checked in a Resolved-layer
  `exhaust()` method before forwarding to the State mutation. (Not built yet —
  no `Resolved*` class currently has an `exhaust()` method; `Exhaustible`
  today is only exercised directly on the State object.)
  
### A Resolved object carries everything needed to *interpret* its entity

More precisely than "one entity's State + its Config": a Resolved object is
**one entity bound with everything needed to interpret it**. Usually that's
just its State and Config. It may also carry immutable values the resolver
looked up from *related* entities, when interpreting this entity requires them.

**Dividing line:** a cross-entity **lookup** belongs to `GameStateResolver`; a
cross-entity **decision** belongs to a Service. Following an ID to a related
entity and reading a value is resolver work, the same kind of ID-to-object step
`_require` already does. Anything involving a rule or judgment across entities
still goes to a Service.

**Guardrails for the extra fields:**
- They must be *lookups*, never decisions.
- They must be *immutable* values (snapshot-safe), such as a `Final` field on
  the related entity. Snapshot only the value needed, never the related
  entity's whole mutable State object.

**Worked example: promissory note text.** A standard promissory note's
functional text names its issuer's color ("the *red* player"). The note's State
stores only `issuing_player_id: str` (the relationship, needed to return the
note to its issuer). The color lives on the issuer's `PlayerState.color`
(`Final`). Rendering the text therefore needs a second entity. Rather than
push that to a Service, the resolver looks up the color and hands the Resolved
object a self-sufficient binding:

```python
@dataclass(frozen=True, kw_only=True)
class ResolvedStandardPromissoryNote(
    BaseResolvedObj[PromissoryNoteCardState, StandardPromissoryNoteConfig]
):
    issuer_color: PlayerColor          # looked up by the resolver, immutable

    @property
    def functional_text(self) -> str:
        return self.config.functional_text.replace(PLAYER_COLOR_TOKEN, self.issuer_color)


@dataclass(frozen=True, kw_only=True)
class ResolvedFactionPromissoryNote(
    BaseResolvedObj[PromissoryNoteCardState, FactionPromissoryNoteConfig]
):
    @property
    def functional_text(self) -> str:
        return self.config.functional_text


type ResolvedPromissoryNote = ResolvedStandardPromissoryNote | ResolvedFactionPromissoryNote
```

```python
class GameStateResolver:
    def resolved_promissory_note(self, note_id: str) -> ResolvedPromissoryNote:
        state = self._require(self._game_state.promissory_notes, note_id, UnknownPromissoryNoteError)
        config = self._ruleset_config.promissory_notes[state.config_id]
        match config:
            case StandardPromissoryNoteConfig():
                issuer = self._require(self._game_state.players, state.issuing_player_id, UnknownPlayerError)
                return ResolvedStandardPromissoryNote(state=state, config=config, issuer_color=issuer.color)
            case FactionPromissoryNoteConfig():
                return ResolvedFactionPromissoryNote(state=state, config=config)
```

Why this shape:
- The ID stays a plain `str` reference; the resolver converts it to a real
  `PlayerColor` by lookup, so no layer ever pretends an ID *is* a color.
- `functional_text` is a no-argument property on both variants, giving callers
  a uniform interface. Making it take a color parameter would split the
  interface (Standard needs one, Faction doesn't) and force every caller to
  know which variant it holds.
- Only the resolver touches both entities. Services call
  `resolver.resolved_promissory_note(id).functional_text` and never reach into
  `PlayerState` for rendering.

## 5. Domain Services

- For genuinely **heterogeneous, cross-entity** rules logic (`MovementService`,
  `CombatService`) — composes multiple `Resolved*` objects, not just one.
- Built on top of `Resolved*` objects, not raw State + manual `config_id` lookups
  — eliminates repeated `ruleset_config.unit(state.config_id)` boilerplate at
  every call site.
- **`BaseService`** (`services/base.py`) holds the one `GameStateResolver` a
  concrete Service needs (`self._resolver`) and a shared
  `_require_ownership(entity, player_id, error_cls)` helper — checks
  `entity.ownable.is_owned_by_player(player_id)` (via the `OwnableEntity`
  Protocol from §3) and raises the caller-supplied `error_cls` if not, so
  every Service gets ownership-checking for free without hand-rolling the
  `if not ...: raise` at each call site.
- **`MovementService`** (`services/movement.py`) is the first realized
  Service: `move_unit(unit_id, destination_system_id, requesting_player_id)`
  resolves both the unit and the destination system through the resolver,
  checks ownership via `_require_ownership`, rejects a no-op move to the
  unit's own system (`SelfMoveError`) and a non-adjacent destination
  (`IllegalDestinationError` — adjacency checked via
  `HexCoordinate.neighbors`, the only legal-destination rule this feature
  currently models), then forwards the single primitive
  (`destination_system_id`) to `UnitState.place_in_system`.
- **Two exception-subclassing styles, chosen by whether the message is fully
  determined by a single id.** `UnknownEntityError`/`OwnershipError` (§3, §4)
  use the **label-only `ClassVar` style**: many near-identical variants exist
  (one per entity type), and each one's message is fully determined by one id
  plus a short label, so a shared parameterized `__init__` on the base class
  pays for itself. `MovementError`'s subclasses (`SelfMoveError`,
  `IllegalDestinationError`) use the **plain-marker style** instead: each
  raise site has richer, situation-specific context to report (both the unit
  id and both system ids, in prose that differs per error) that doesn't
  reduce to "fill in one label," so the message is built at the raise site
  and the subclass exists only to be caught/distinguished by type. Don't
  default to the `ClassVar` style everywhere — use it only when the
  near-identical-variants condition actually holds.

## 6. State-to-state relationship rules ("derive, don't store both sides")

Pick exactly **one side** to store a reference on — never both, never store a
computed reverse-list that could drift out of sync. Classify by cardinality:

1. **1:many** → store the "1" reference on each of the "many" (e.g.
   `UnitState.location.location_id`, a system/planet/ship id depending on
   `UnitLocation.loc_type` — see `state/unit/location.py` — not a `unit_ids`
   list on `SystemState`).
2. **1:many, optional on the many side** → same as (1), just `Optional`
   (e.g. `SecretObjectiveCardState`'s composed `ownable.owned_by_player_id: str | None`).
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

- Lifecycle modeled via a `SecretObjectiveZone` enum (`IN_DECK`, `IN_HAND`,
  `SCORED`, `REVEALED`) on the card — not separate booleans (avoids
  representable-but-invalid states like `scored=True, owner=None`).
- Ownership (rule 2) is the generic `PlayerOwnableMixin`/`ownable` composition
  from §3, not a bespoke `owner_player_id` field — `give_to_player` forwards
  to `self.ownable.set_owner(player_id)`; permanent once set, independent of
  the `zone` transitions.
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
  that's `RulesetConfig`'s job). Currently modeled as `X | None = None` fields
  directly on `GameState` (`naalu_token`, `nekro_assimilator_tokens`,
  `creuss_wormhole_tokens` — the latter two `tuple[X, X] | None` since each of
  those factions has exactly two tokens when present) — there's no separate
  `SpecialTokenStates` aggregate class wrapping them.
- Construction *should* belong in `new_game()` composition logic once that
  decision is implemented — reaching into which factions were picked to decide
  which tokens exist is a genuine setup *decision*, not a mechanical
  derivation, so it doesn't belong in `__post_init__`, and it's the same
  category of work `GameState.new_game()` already does for map layout,
  factions, etc. (Not built yet — `GameState.new_game(players, systems,
  planets)` doesn't take faction ids or a `RulesetConfig` today, and simply
  leaves all three fields at their `None` default regardless of which
  factions are in the game.)
- Token → owner is rule 1/2 shape: the `PlayerOwnableMixin`/`ownable`
  composition from §3 stored on the token (often effectively non-optional in
  practice, since these tokens are only ever constructed once an owner is
  already known, even though `_PlayerOwnable.owned_by_player_id` is typed
  `str | None`).
