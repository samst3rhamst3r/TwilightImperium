# Architectural Decision Records

Point-in-time records of *why* a significant, hard-to-reverse decision was
made — distinct from `ARCHITECTURE.md`, which is the living, continuously
updated technical reference for the *current* state of the design.

**An ADR is written once and never edited to match later changes.** If a
decision is later reversed or refined, write a new ADR that supersedes it
(link back to the one it supersedes) rather than rewriting history —
`ARCHITECTURE.md` is where the *current* truth lives; this folder is the
paper trail for *why things got that way*.

## When to write one

A new significant, hard-to-reverse architectural decision — not every design
choice. Rule of thumb: if reversing it later would mean touching many files
across layers, or re-litigating a debate that took real back-and-forth to
settle, it's ADR-worthy. A local implementation choice within one class
isn't — that belongs in a code comment or, if it affects the whole layer, an
`ARCHITECTURE.md` update.

## Format

Copy [`0000-template.md`](0000-template.md). Number sequentially
(`0001-`, `0002-`, ...), kebab-case title.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-layered-architecture-one-way-dependencies.md) | Layered architecture with one-way dependencies | Accepted |
| [0002](0002-derive-dont-store-state-relationships.md) | Derive-don't-store for State-to-State relationships | Accepted |
| [0003](0003-serializable-as-single-cooperative-terminal.md) | `Serializable` as the single save/load cooperative-chain terminal | Accepted |
