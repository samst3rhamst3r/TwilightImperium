# AGENTS.md

Tool-agnostic entry point for AI coding agents working in this repository.
If you're Claude Code, also read `CLAUDE.md` for Claude-specific workflow
mechanics (slash commands, plan-mode conventions) — this file covers what's
true regardless of which agent is reading it.

## What this is

A Python implementation of the board game Twilight Imperium: a layered rules
engine (`config/` → `state/` → `setup/` → `resolved/` → `services/` →
`orchestration/`), not yet a playable app — see Project Status below for
which layers exist.

## Before making any change

1. Read `.specify/memory/constitution.md` — the highest-precedence governance
   document in this repo. Its five principles (spec-before-code, layered
   architecture, derive-don't-store, Config immutability/State mutability,
   test coverage before completion) are non-negotiable, not suggestions.
2. Read the relevant section of `ARCHITECTURE.md` before touching `config/`,
   `state/`, `setup/`, `resolved/`, or `services/` — it's the detailed
   technical reference for *how* to satisfy the constitution's principles
   (mixin patterns, save/load design, the per-layer ownership table in §1).
3. For anything touching more than one file, or where the approach isn't
   obvious: write a spec first, per the constitution's Development Workflow
   section and `specs/TEMPLATE.md`.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
```

Python 3.14. No `requires-python` pinned in `pyproject.toml` yet.

## Running tests

```bash
pytest                        # everything, from repo root
pytest tests/test_config       # one layer at a time while iterating
pytest tests/test_state
```

`pyproject.toml` sets `pythonpath = "src"` — tests import as `from app...`
without an editable install.

## Project structure

```
src/app/
  config/       # static ruleset data — loaded once, frozen, shared
  state/        # live per-game data — mutable, never frozen
  setup/        # pre-game setup — GameSetupSession / GameSetup (not yet built)
  resolved/     # binds one State + its Config for one operation
  services/     # cross-entity rules logic (not yet built)
  orchestration/# turn/phase sequencing (not yet built)
  geometry/     # hex-coordinate math, no game-concept awareness

data/           # raw YAML ruleset content
tests/          # mirrors src/app/** one-for-one, plus per-layer *_invariants.py
specs/          # one folder per feature, spec+plan combined (see specs/TEMPLATE.md)
docs/adr/       # architectural decision records — the *why*, point-in-time
```

## Project status

| Layer | Status |
|---|---|
| `config/` | Built, tested |
| `state/` | Built, tested — 269 passing (`specs/001-state-objects/plan.md`) |
| `setup/` | Designed (`ARCHITECTURE.md` §1), not yet implemented |
| `resolved/` | In progress — 6 `Resolved*` classes so far (`specs/002-resolved-layer/plan.md`) |
| `services/`, `orchestration/` | Not yet started |

## Where to look for *why*, not just *what*

- **`ARCHITECTURE.md`** — living technical reference, current state of truth,
  updated whenever a design decision changes.
- **`docs/adr/`** — point-in-time records of *why* a significant decision was
  made the way it was, kept even after the design has since evolved further.
- **`.specify/memory/constitution.md`** — non-negotiable process/architectural
  rules; governs if it ever conflicts with anything else.
