# Spec: <feature name>

## Overview
One or two sentences: what this change does and why.

## Requirements
- Bullet list of concrete, testable behaviors this feature must satisfy.
- Prefer specific over vague: "rejects a move to a non-adjacent system" not
  "handles movement correctly."

## Out of scope
Explicitly list what this spec does *not* cover, especially anything adjacent
that might otherwise get pulled in scope-creep style.

## Design
- Files/interfaces involved (existing files to modify, new files to create).
- Which architectural layer(s) this touches (Config / State / Resolved /
  Services / Orchestration) — see ARCHITECTURE.md.
- Any new State-to-State relationships: classify cardinality per
  ARCHITECTURE.md §6 (1:many, many:many, etc.) and state which side stores
  the reference.
- Any new mixins/traits: state whether it's a dataclass mixin, Protocol, or
  ABC per the §3 decision test, and why.

## Open questions
Anything genuinely undecided — surface these rather than silently picking
an answer during implementation.

## Verification
The concrete, end-to-end check that proves this works. Not "looks correct" —
an actual command, test, or reproducible scenario.
- [ ] e.g. `pytest tests/state/test_<feature>.py` passes
- [ ] e.g. manual scenario: construct X, call Y, assert Z
