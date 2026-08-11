"""Structural invariants that must hold for *every* State dataclass.

Mirrors ``tests/test_config/test_config_invariants.py``'s sweep pattern
(via ``pytest_generate_tests`` in conftest.py), adapted for State's
conventions - which oppose Config's on the frozen question: Config
dataclasses must be frozen; State dataclasses must NOT be, since they're
mutable per-game data and ``frozen=True`` is structurally incompatible with
``Serializable.load()``'s ``cls.__new__(cls)`` + mutate pattern (see
ARCHITECTURE.md section 3). Both layers require ``kw_only=True`` and no
``slots=True`` - State has zero exemptions from either (unlike Config's one
deliberate ``MapConfig`` case).
"""
import dataclasses

def test_state_dataclass_is_not_frozen(state_dataclass: type) -> None:
    assert not state_dataclass.__dataclass_params__.frozen, (
        f"{state_dataclass.__name__} must not be frozen - State objects are "
        "mutable per-game data, and frozen=True is structurally incompatible "
        "with Serializable.load()'s cls.__new__(cls) + mutate pattern "
        "(see ARCHITECTURE.md section 3)."
    )

def test_state_dataclass_is_kw_only(state_dataclass: type) -> None:
    params = state_dataclass.__dataclass_params__
    if not params.init:
        return  # no generated __init__ (e.g. Serializable) - kw_only is moot
    assert params.kw_only, f"{state_dataclass.__name__} must be declared with kw_only=True"

def test_state_dataclass_has_no_slots(state_dataclass: type) -> None:
    assert not state_dataclass.__dataclass_params__.slots, (
        f"{state_dataclass.__name__} must not use slots=True - combining 2+ "
        "slotted trait mixins raises TypeError: multiple bases have instance "
        "lay-out conflict (see ARCHITECTURE.md section 3)."
    )

def test_state_dataclass_field_names_are_unique(state_dataclass: type) -> None:
    """Guards against a mixin silently shadowing/duplicating another mixin's
    field - dataclasses.fields() would otherwise just report the last one."""
    names = [f.name for f in dataclasses.fields(state_dataclass)]
    assert len(names) == len(set(names)), (
        f"{state_dataclass.__name__} has duplicate field names: {names}"
    )

def test_at_least_one_state_dataclass_was_discovered(all_state_dataclasses: list[type]) -> None:
    """Sanity check on the discovery mechanism itself - if this ever starts
    failing, the sweep above is silently checking nothing."""
    assert len(all_state_dataclasses) > 10

def test_at_least_one_state_enum_was_discovered(all_state_enums: list[type]) -> None:
    assert len(all_state_enums) >= 1
