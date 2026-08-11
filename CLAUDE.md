# Twilight Imperium App

Python implementation of the board game Twilight Imperium.

## Project context
See @ARCHITECTURE.md for the full architecture reference (layering, mixin
patterns, save/load design, derive-don't-store relationship rules). Read the
relevant section before touching `config/`, `state/`, `resolved/`, or
`services/`. Update it when a design decision changes.

## Workflow — spec before code
For anything touching more than one file, or where the approach isn't obvious:

1. Write a spec first. Copy `specs/TEMPLATE.md` to `specs/<feature-name>/SPEC.md`.
   Prefer interviewing me for it: "Interview me in detail using AskUserQuestion,
   then write the spec." Keep specs in git — they're source of truth, not scratch.
2. Enter plan mode before implementing. Turn the spec into a numbered plan.
3. Implement against the plan in a fresh session/context.
4. Verify against the spec's end-to-end check before calling it done — show the
   evidence (test output, not just "looks done").

Skip the spec for single-file, obvious-diff changes (typo fixes, renames, etc.).

## Code style
- `kw_only=True` on every `state/`/`config/` dataclass, with one deliberate
  exception: `MapConfig` — its `tiles` shape is encoded as a bare positional
  list of `[q, r]` pairs in `data/objs/map/*.yaml` to keep the hex-grid
  layout readable in the file, so `kw_only=True` would fight that shape.
  Don't "fix" this back to `kw_only=True`.
- Apply the mixin decision test in ARCHITECTURE.md §3 (dataclass mixin vs.
  Protocol vs. ABC) before adding any new trait — don't default to Protocol
  out of habit.
- New State-to-State relationships: apply the derive-don't-store cardinality
  rules in ARCHITECTURE.md §6 before adding a field.

## Testing
Run tests before considering any implementation task complete.

Usage, from the top-level directory of this workspace: `pytest` (bare, from
repo root) collects and runs both `tests/test_config` and `tests/test_state`
cleanly. While iterating on one layer, `pytest tests/test_config` or
`pytest tests/test_state` individually gives faster feedback and keeps
failures attributable to the layer you're actually changing.

### Test layout
Test packages mirror their source package one-for-one (`tests/test_config/objs/test_unit/`
↔ `app/config/objs/unit/`, etc.) — a per-class test module sits next to the
class it covers, for behavior reflection can't check (mixin semantics,
`__post_init__` validation, real-data spot checks). A single suite-wide
`test_<layer>_invariants.py` (see `test_config_invariants.py`) covers
structural rules that must hold for *every* class in the layer, via the
sweep pattern below — it doesn't mirror a source file because it isn't
about one class.

### Fixtures (`conftest.py`)
- **Session-scoped real-data fixture** — load the actual `data/` tree once
  per test session (`ruleset_config`, via `RulesetConfig.load(data_dir)`),
  rather than hand-built fixture data. Catches drift between real YAML
  content and the typed shape that hand-rolled fixtures would miss, at
  near-zero cost since it's loaded once and shared.
- **Discovery fixtures** — walk the package under test with `pkgutil.walk_packages`
  + `inspect.getmembers` to collect every dataclass/enum actually defined
  there (`all_config_dataclasses`, `all_config_enums`), rather than a
  hand-maintained list. New classes get swept automatically.
- **Factory fixtures, not asserting fixtures** — a fixture returns a
  *callable* that computes and returns a result (e.g. a list of violation
  strings, empty if clean); the `assert` itself always lives in the `test_`
  function, never inside a fixture. Keeps failure messages attributable to
  a specific test and keeps fixtures reusable across different assertions.

### Loader isolation
Test each per-type loader function (`load_unit_data`, `load_tech_data`, etc.)
individually against the real data tree, in addition to (not instead of) a
full `RulesetConfig.load()` test. A composed-only test means one malformed
field in one YAML file fails the *entire* suite's worth of downstream
assertions instead of just that loader's — isolating the loader calls keeps
failures attributable to the actual broken piece.

### Structural sweeps via `pytest_generate_tests`
For invariants that must hold across *every* class in a layer (frozen,
`kw_only=True`, no mutable-container fields, unique field names, …), use
`pytest_generate_tests` in `conftest.py` to parametrize a test function over
the discovery fixtures' results (one test-id per discovered class), rather
than writing one hand-copied test per class. A new Config/State class is
covered automatically the moment it's added to the package — no one has to
remember to write its structural test. Reserve hand-written per-class tests
for behavior the sweep can't express (see Test layout above).

### Runtime immutability, not just declared types
Two complementary checks, both needed — a correct type hint doesn't
guarantee a correct runtime value:
- **Declared-type check** — walk a dataclass's `get_type_hints()` and flag
  any bare `dict`/`list`/`set` (including nested inside `tuple[...]`/
  `MappingProxyType[...]`), since only `tuple`/`MappingProxyType` are
  allowed for sequence/mapping fields.
- **Runtime object-graph check** — recursively walk an actual *instance*
  (dataclass fields → tuple elements → `MappingProxyType` keys/values),
  flagging any real `list`/`dict`/`set` encountered anywhere in the graph,
  with cycle protection via a `seen: set[id(...)]`. Catches a loader that
  declares the right type hint but forgets to convert a nested raw list
  before construction — a bug the declared-type check alone can't see.

### General principles
- Prefer exercising real `data/` content over synthetic fixtures wherever
  feasible — this repo's Config/State shapes are meant to match real game
  data exactly, so synthetic data can pass while real data fails.
- A discovery-sweep test suite should include one sanity check on the
  discovery mechanism itself (e.g. `assert len(all_config_dataclasses) > 10`)
  — if discovery silently starts returning zero classes, every parametrized
  test in the sweep silently passes on nothing instead of failing loudly.