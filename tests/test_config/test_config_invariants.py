"""Structural invariants that must hold for *every* Config dataclass/enum.

Unlike the rest of this suite, this module does not mirror a single source
file - it sweeps everything discovered under ``app.config`` (via
``pytest_generate_tests`` in conftest.py) so that a new Config class or enum
added later is covered automatically, without anyone needing to remember to
add a dedicated test for it. Per-class test modules still exist alongside
this for behavior that reflection can't check (mixin semantics, __post_init__
validation, real-data spot checks).
"""
from app.config.shared.enum import ConfigEnum

def test_config_dataclass_is_frozen(config_dataclass: type) -> None:
    assert config_dataclass.__dataclass_params__.frozen, (
        f"{config_dataclass.__name__} must be a frozen dataclass"
    )

def test_config_dataclass_is_kw_only(config_dataclass: type) -> None:
    params = config_dataclass.__dataclass_params__
    if not params.init:
        return  # no generated __init__ (e.g. BaseConfigObj) - kw_only is moot
    assert params.kw_only, f"{config_dataclass.__name__} must be declared with kw_only=True"

def test_config_dataclass_has_no_mutable_container_fields(
    config_dataclass: type, mutable_container_violations
) -> None:
    violations = mutable_container_violations(config_dataclass)
    assert not violations, "\n".join(violations)

def test_config_dataclass_field_names_are_unique(config_dataclass: type) -> None:
    """Guards against a mixin silently shadowing/duplicating another mixin's
    field - dataclasses.fields() would otherwise just report the last one."""
    import dataclasses
    names = [f.name for f in dataclasses.fields(config_dataclass)]
    assert len(names) == len(set(names)), (
        f"{config_dataclass.__name__} has duplicate field names: {names}"
    )

def test_config_enum_values_match_lowercased_names(config_enum: type) -> None:
    """StrEnum's auto() lower-cases the member name by default - this is the
    property ConfigEnum's YAML-loading validation (_missing_) relies on."""
    for member in config_enum:
        assert member.value == member.name.lower(), (
            f"{config_enum.__name__}.{member.name} has value {member.value!r}, "
            f"expected the lower-cased member name {member.name.lower()!r}"
        )

def test_at_least_one_config_dataclass_was_discovered(all_config_dataclasses: list[type]) -> None:
    """Sanity check on the discovery mechanism itself - if this ever starts
    failing, the sweep above is silently checking nothing."""
    assert len(all_config_dataclasses) > 10

def test_at_least_one_config_enum_was_discovered(all_config_enums: list[type]) -> None:
    assert len(all_config_enums) > 5

def test_yaml_sourced_enums_are_configenum_subclasses() -> None:
    """Enums whose *values* come from raw YAML strings must inherit
    ConfigEnum (not just SerializableEnum), since ConfigEnum._missing_ is
    what enforces "YAML values must already be lower-cased" instead of
    silently accepting e.g. "Cultural" as a match for CULTURAL.

    This list is intentionally hand-maintained rather than discovered by
    reflection: "is this enum's data YAML-sourced" is domain knowledge, not
    something inspectable from the class alone. Enums deliberately excluded
    here (PlayerColor, UnitLocationType) are assigned/derived by app logic,
    never parsed out of a YAML value, so ConfigEnum's case-strictness
    doesn't apply to them.
    """
    from app.config.objs.ability import AbilityID
    from app.config.objs.agenda import AgendaType, AgendaVoteScenarioType
    from app.config.objs.map import MapShape
    from app.config.objs.objective import ObjectiveType
    from app.config.objs.planet import PlanetTrait
    from app.config.objs.system import AnomalyType, TileColor, WormholeType
    from app.config.objs.tech import TechType
    from app.config.objs.unit import UnitClass

    yaml_sourced_enums = (
        AbilityID,
        AgendaType,
        AgendaVoteScenarioType,
        MapShape,
        ObjectiveType,
        PlanetTrait,
        AnomalyType,
        TileColor,
        WormholeType,
        TechType,
        UnitClass,
    )
    for enum_cls in yaml_sourced_enums:
        assert issubclass(enum_cls, ConfigEnum), (
            f"{enum_cls.__name__} carries values parsed from YAML data and must "
            "inherit from ConfigEnum, not just SerializableEnum"
        )
