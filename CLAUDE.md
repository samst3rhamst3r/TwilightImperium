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
- `kw_only=True` on every `state/`/`config/` dataclass (see ARCHITECTURE.md
  field-ordering notes on mixed default/non-default fields).
- Apply the mixin decision test in ARCHITECTURE.md §3 (dataclass mixin vs.
  Protocol vs. ABC) before adding any new trait — don't default to Protocol
  out of habit.
- New State-to-State relationships: apply the derive-don't-store cardinality
  rules in ARCHITECTURE.md §6 before adding a field.

## Testing
Run tests before considering any implementation task complete.
Usage:
  On any OS, starting from the top-level directory of this workspace: "python tests"