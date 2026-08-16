# Twilight Imperium App

A Python implementation of the board game *Twilight Imperium* — a rigorously
layered rules engine, built spec-first, intended to eventually serve as the
core rules engine behind a mobile board-game platform (a local WebSocket/HTTP
server process, thin client apps handling rendering).

This is a rules-engine project, not yet a playable app — see **Project
Status** below for what's built.

## Architecture, in one sentence

Static ruleset data (`config/`) is strictly separated from live per-game data
(`state/`), which is never held or mutated by anything above it except
through a `Resolved*` binding layer (`resolved/`) and, above that, cross-entity
rules logic (`services/`) orchestrated by turn/phase sequencing
(`orchestration/`) — one-way dependencies throughout, enforced as a
constitutional rule, not just a convention.

For the full design — layering rationale, mixin patterns, save/load
mechanics, the State-relationship cardinality rules — see
**[ARCHITECTURE.md](ARCHITECTURE.md)**. For *why* specific significant
decisions were made, see **[docs/adr/](docs/adr/)**.

## Getting started

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate    # macOS/Linux
pip install -r requirements.txt

pytest   # from repo root
```

Python 3.14.

## Project status

| Layer | Status |
|---|---|
| `config/` | Built, tested |
| `state/` | Built, tested (269 tests passing) |
| `setup/` | Designed, not yet implemented |
| `resolved/` | In progress (6 `Resolved*` classes so far) |
| `services/` / `orchestration/` | Not yet started |

## Development workflow

This project follows a spec-driven development workflow — see
[`.specify/memory/constitution.md`](.specify/memory/constitution.md) for the
governing rules, and [`specs/`](specs/) for feature specs (one folder per
feature, spec and plan combined per `specs/TEMPLATE.md`).

If you're an AI coding agent working in this repo, start with
[`AGENTS.md`](AGENTS.md).

## License

Third-party dependency licenses are listed in
[`THIRD-PARTY-LICENSES.md`](THIRD-PARTY-LICENSES.md).
