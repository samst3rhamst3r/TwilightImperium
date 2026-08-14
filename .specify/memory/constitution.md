<!--
Sync Impact Report
- Version change: (unratified template) → 1.0.0
- Rationale for 1.0.0: Initial ratification. The file previously on disk was the raw
  scaffold with every [PLACEHOLDER] token still unfilled — no prior version was ever
  adopted, so this is not an amendment to an existing constitution but its first
  adoption (MAJOR.0.0 per semver-for-governance convention).
- Modified principles: n/a (none existed previously)
- Added sections:
  - Core Principles I–V (Spec-Before-Code; Layered Architecture & One-Way
    Dependencies; Derive-Don't-Store State Relationships; Config Immutability /
    State Mutability / Primitive-Only State Methods; Test Coverage Before
    Completion)
  - Data & Ingestion Constraints (Section 2)
  - Development Workflow (Section 3)
  - Governance
- Removed sections: none
- Content source: derived from the existing, actively-followed project docs
  (CLAUDE.md "Workflow", "Code style", "Testing" sections; ARCHITECTURE.md §1–§6),
  not invented from scratch — this file codifies what those docs already establish
  as non-negotiable, so it can be checked by the speckit plan/tasks/analyze
  commands without re-deriving it from prose each time.
- Follow-up TODOs:
  - None blocking. RATIFICATION_DATE is set to the date of this first adoption
    (no earlier ratification exists to preserve).
-->

# Twilight Imperium App Constitution

## Core Principles

### I. Spec-Before-Code
Any change touching more than one file, or whose approach is not obvious, MUST
be preceded by a written spec before implementation begins. Single-file,
obvious-diff changes (typo fixes, renames, and similarly mechanical edits) are
exempt. Specs are kept in git under `specs/<feature-name>/SPEC.md` — they are
source of truth, not scratch notes, and MUST NOT be discarded once written.
**Rationale**: This codebase's layering and derive-don't-store rules
(Principles II–III) are easy to violate by accident when code is written
before the relationships are thought through; a spec forces that thinking to
happen before code exists to defend.

### II. Layered Architecture, One-Way Dependencies
The application MUST maintain its layer separation — `data/`, `config/`,
`state/`, `resolved/`, `services/`, `orchestration/`, with `geometry/` as
shared, dependency-free vocabulary. Dependency direction is one-way only
(`resolved` depends on `config` + `state`; `services` depends on `resolved`;
`orchestration` depends on `services`); a lower layer importing from a higher
one is a constitution violation. The orchestrator MUST NOT touch raw
`GameState` containers directly — it may only call `Resolved*` objects and
Domain Services. Placement of any new class, field, or method MUST be checked
against the "who owns what" table and one-line ownership tests in
ARCHITECTURE.md §1 before being added.
**Rationale**: The one-way boundary is what keeps static ruleset data,
live per-game data, and cross-entity rules logic independently testable and
independently reasoned-about; once a layer boundary is crossed once, it tends
to be crossed again at the next expedient moment.

### III. Derive, Don't Store — State Relationship Discipline
Every new State-to-State relationship MUST store a reference on exactly one
side, chosen by the cardinality rules in ARCHITECTURE.md §6 (1:many,
1:optional, many:many, optional:optional) — never on both sides, and never as
a stored, separately-synced reverse list. "Many" queries and counts (e.g.
"objects held by X", "count of Y") MUST be derived on demand via filter
methods, never stored as an incrementable counter or maintained list.
**Rationale**: A reverse-reference or counter that isn't the single source of
truth WILL drift out of sync with the side that is; deriving on demand costs
an O(1)-ish lookup and eliminates the entire class of drift bugs.

### IV. Config Immutability, State Mutability, Primitive-Only State Methods
Config objects MUST stay frozen/immutable and independent of any specific
game in progress. State objects MUST reference Config only by `config_id:
str`, never by holding a direct Config object reference. State methods MUST
accept only primitives or already-decided values — never a Config object;
any computation that requires resolving Config belongs at the Resolved layer
or above, which resolves Config and then calls the simpler State method with
a concrete value. Before adding any new shared trait, the mixin decision test
in ARCHITECTURE.md §3 (dataclass mixin vs. `Protocol` vs. `ABC`) MUST be
applied rather than defaulting to `Protocol` out of habit.
**Rationale**: This is what keeps State serializable, alias-safe, and
testable without a live Config instance, and keeps "what does this card
currently do" logic in exactly one place (Resolved) instead of leaking into
State.

### V. Test Coverage Before Completion
No implementation task is considered complete until `pytest`, run bare from
the repository root, passes cleanly across both `tests/test_config` and
`tests/test_state`. Every new Config/State class MUST be covered
automatically through the structural sweep pattern
(`pytest_generate_tests` over the discovery fixtures) rather than requiring
someone to remember to hand-write its structural test; hand-written
per-class tests are reserved for behavior the sweep genuinely cannot express
(mixin semantics, `__post_init__` validation, real-data spot checks).
Per-type loaders MUST be tested individually against real `data/` content, in
addition to — not instead of — a full `RulesetConfig.load()` test, so a
malformed field in one YAML file fails only its own loader's test rather than
the entire suite.
**Rationale**: A task that "looks done" but hasn't been run against
`pytest` is not verified; the sweep pattern is what keeps new classes from
silently escaping structural coverage as the codebase grows.

## Data & Ingestion Constraints

Any ingestion of file content in this repository (documentation sweeps,
code-generation prompts, fixture construction, bulk search/analysis) MUST
ignore folders and files enumerated in `.gitignore`. If honoring that
exclusion would conflict with what a task actually needs, the conflict MUST
be raised via `AskUserQuestion` to get an explicit exception before
proceeding — it MUST NOT be assumed silently.

## Development Workflow

For any change in scope under Principle I, the process is:

1. **Spec**: Copy `specs/TEMPLATE.md` to `specs/<feature-name>/SPEC.md`.
   Prefer interviewing the user in detail (via `AskUserQuestion`) to produce
   it, rather than guessing at requirements.
2. **Plan**: Enter plan mode before implementing; turn the spec into a
   numbered, concrete plan.
3. **Implement**: Execute against the plan in a fresh session/context, so
   implementation isn't biased by the exploratory reasoning that produced the
   plan.
4. **Verify**: Before calling the task done, check it against the spec's
   end-to-end check and show the evidence — actual test output or a
   reproducible command result, never "looks done" asserted without proof.

`config/`, `state/`, `resolved/`, and `services/` changes additionally
require reading the relevant section of `ARCHITECTURE.md` before touching
that layer, and updating `ARCHITECTURE.md` itself whenever a design decision
changes it.

## Governance

This constitution is the highest-precedence governance document in this
repository for process and architectural-boundary rules. `CLAUDE.md` and
`ARCHITECTURE.md` remain the detailed technical reference for *how* to
satisfy these principles (mixin patterns, save/load design, per-layer
ownership tables, etc.); if a future edit to either ever contradicts this
constitution, this constitution governs and the conflicting document MUST be
corrected to match.

**Amendments**: Made only via the `/speckit-constitution` command, which
regenerates this file from the current template plus recorded project
context. Every amendment MUST update the Sync Impact Report at the top of
this file and bump the version per semantic versioning:
- **MAJOR** — backward-incompatible removal or redefinition of a principle or
  governance rule.
- **MINOR** — a new principle added, or existing guidance materially
  expanded.
- **PATCH** — clarification, wording, or other non-semantic refinement.

**Compliance review**: Any spec, plan, or implementation produced under the
Development Workflow above MUST be checked against these principles before
being marked complete. A deliberate deviation (e.g. the documented
`MapConfig.tiles` exception to `kw_only=True` in `CLAUDE.md`) MUST be
recorded as an explicit, justified exception in the relevant doc rather than
silently violating the principle.

**Version**: 1.0.0 | **Ratified**: 2026-08-13 | **Last Amended**: 2026-08-13
