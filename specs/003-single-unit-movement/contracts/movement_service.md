# Contract: `MovementService.move_unit`

This project has no HTTP/CLI surface — its "interface" is the Domain
Service's public Python method, the sanctioned entry point Orchestration
(once built) and tests call. This document is that contract.

## Signature

```python
class MovementService(BaseService):
    def move_unit(
        self,
        *,
        unit_id: str,
        destination_system_id: str,
        requesting_player_id: str,
    ) -> None:
        ...
```

Constructed as `MovementService(resolver)` where `resolver` is a
`GameStateResolver` already bound to the `GameState` + `RulesetConfig` in
play (`BaseService.__init__`, unchanged).

## Inputs

| Parameter | Type | Meaning |
|---|---|---|
| `unit_id` | `str` | `UnitState.instance_id` of the unit to move. |
| `destination_system_id` | `str` | `SystemState.config_id` (per-game system id, e.g. `"sys_18"`) of the requested destination. |
| `requesting_player_id` | `str` | The id of the player making the request — checked against the unit's current owner. |

All three are keyword-only, primitive `str` ids — no Config or State object
is ever passed in (ARCHITECTURE.md §1/§4: State-and-below methods take only
primitives/already-decided values).

## Output

`None` on success. The only observable effect is
`GameState.deployed_units[unit_id].location` now pointing at
`destination_system_id` — nothing else in `GameState` changes (FR-007).

## Errors

All exceptions are defined in `app.services.movement` and share a common
`MovementError` base, so a caller can catch broadly (`except MovementError`)
or narrowly. Every one of them leaves `GameState` completely unchanged —
none of them partially apply the move.

| Exception | Condition | Spec ref |
|---|---|---|
| `UnknownUnitError` | No unit with `unit_id` exists in `game_state.deployed_units`. | FR-006 |
| `UnknownSystemError` | No system with `destination_system_id` exists in `game_state.systems`. | FR-006 |
| `UnitOwnershipError` | `requesting_player_id` does not own the unit. | FR-004 |
| `SelfMoveError` | `destination_system_id` equals the unit's current system id. | FR-005 |
| `IllegalDestinationError` | `destination_system_id` is a real, different system, but is not a direct hex neighbor of the unit's current system. | FR-003 |

Checked in that order (first match wins) — see
`research.md` Decision 4 for why.

## Example usage

```python
resolver = GameStateResolver(game_state, ruleset_config)
movement = MovementService(resolver)

movement.move_unit(
    unit_id="a1b2c3...",
    destination_system_id="sys_25",
    requesting_player_id="red",
)
# unit is now located in "sys_25"

try:
    movement.move_unit(
        unit_id="a1b2c3...",
        destination_system_id="sys_99",
        requesting_player_id="blue",
    )
except UnitOwnershipError:
    ...  # blue doesn't own this unit; game_state is unchanged
```

## Explicitly out of contract (spec Assumptions)

Not checked, not attempted, no partial support: wormhole adjacency, anomaly
movement restrictions, fleet capacity/supply, "system already activated"
tactical-action rules, command-token spend, combat-trigger detection on
arrival. A future feature extends this contract (most likely: an additional
optional parameter or a second Service method), not this one.
