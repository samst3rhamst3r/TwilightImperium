# Spec: State-Object Layer

## Overview
The state object layer is similar to the Config layer, except that its dataclasses
are meant to hold live, mutable data during gameplay. Therefore, their contents
should never be frozen, but rather accessible, queriable, mutable, and serializable.

## Requirements
- Every State object class cannot be frozen in state once instantiated, though they may have individual frozen attributes
- Every State object must be Serializable - to save & loadable from save
- The file/folder structure of src/app/state should generally follow src/app/config, but it may deviate as State-specific functionality is discovered
- State objects should not hold live instances of actual game objects, except for the "GameState" class instance
- State object data typically only holds simple primitives, simple containers of primitives, or string references to other State objects
- Methods on State objects should be scoped to what those State objects can do to their own internal data - edit, query, and derive directly from their data; for purposes related to higher layers that will manage that State object. Some behavior can be deferred until such layering is known.
- Loading from save dictionary should recreate an exact replica object that existed before creating the save dictionary
- There must be a new_game functionality which propagates default construction of State objects based upon game rules. Those rules are on PDF and can be requested

## Out of scope
- These State objects should NOT require any direct references to Config layer dataclass objects - that will be resolved at a higher layer

## Design
- Files will be contained under src/app/state, touching only the State architectural layer - see ARCHITECTURE.md.
- Refer to ARCHITECTURE.md on questions related to designing the data model for varying cardinality of data relationships - 1:1, 1:many, etc.
- Inheritance shall be used for the Serializable capability, as that is the fundamental aspect of these State objects
- Other capabilities can also use inheritance for class-specific "mixin" functionality, but that can done via regular inheritance or Protocols
- The `base` folder is where reusable mixins and the base inheritable dataclass are located. Everything else is a relevant game item that leverages those classes compositionally
- The naming of superclasses and mixins should indicate whether a particular functionality is optional or required. The base Serializable class is exempt from this usage of language

## Open questions
- I am not sure about whether the usage of `Final` on frozen dataclass attributes is relevant. There are some attributes that don't change after object creation, but the dataclasses cannot leverage `frozen=True` because mutable state elsewhere in the dataclass is required. A more robust mechanism may be required, as `Final` only helps with static type-checkers, not runtime enforceability
- **Secret objective scored-ownership**: Should `SecretObjectiveCardState.owner_player_id`
  be retained permanently once set (per ARCHITECTURE.md section 6's worked example) or
  released on scoring (current code, `release_owner_and_score`)? There is a game effect
  that converts a scored secret objective into a publicly-scoreable one, at which point
  per-player ownership becomes meaningless — but this needs to be weighed against the
  common-case (~99%) states: held in a player's hand, scored by a player, or sitting in
  the deck. Unresolved; code currently releases ownership on score, relying on
  `PlayerState.scored_objective_card_ids` as the sole record of who scored it.
- **Agenda/Tech card population strategy**: `GameState.agenda_cards`/`tech_cards`
  (`MappingProxyType[str, AgendaCardState | TechCardState]`, holding only the mutable
  `exhausted` state a subset of Agenda/Tech cards can have per `data/text_objs/{agendas,techs}.yaml`)
  — should these be populated *sparsely* (only entries for cards that have actually been
  exhausted at some point) or *densely* (one entry per Agenda/Tech `config_id` that exists
  in `RulesetConfig`, from game start)? Related: unlike Tech (never "drawn"), Agenda cards
  are physically drawn from a real deck each Agenda phase in the rulebook — whether
  `agenda_cards` eventually needs `CardDeckState`-style deck/discard semantics instead of
  (or alongside) a flat `MappingProxyType` is the same category of unresolved shape
  question. This reverses half of an earlier decision (commit `c875fcb`, "a tech card has
  no state at all") — that commit's *ownership* conclusion (tech ownership belongs on
  `PlayerState.researched_tech_ids`, many:many) remains correct and is unchanged; only its
  "no state at all" claim is reversed here, given the real per-card exhaustion effects that
  commit didn't account for. Leave both questions unresolved until `new_game()` design
  settles them.

## Verification
The concrete, end-to-end check that proves this works. Not "looks correct" —
an actual command, test, or reproducible scenario.
- [ ] `pytest tests/test_state` passes (or `pytest tests\\test_state` on Windows) after test modules have been created and comprehensively filled with tests related to their companion module(s)
- [ ] The calling system can call "new_game" classmethod on GameState object, and the correct definition of a new game according to game rules is fully created without additional input from the calling entity
