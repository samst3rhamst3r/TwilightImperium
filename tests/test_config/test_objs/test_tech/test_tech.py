"""Mirrors src/app/config/objs/tech/tech.py."""
import pytest

from app.config.fromdict import FromDictMixin
from app.config.objs.tech import AssimilatorTechConfig, StandardTechConfig, TechConfig, TechType
from app.config.objs.mixins import CanHaveFactionExclusivity, RequiresFactionExclusivity, RequiresFunctionalText, CanBeExhaustible
from app.config.objs.named import NamedConfigObj

def test_tech_config_composes_the_expected_mixins() -> None:
    assert issubclass(TechConfig, NamedConfigObj)
    assert issubclass(TechConfig, RequiresFunctionalText)
    # Faction exclusivity isn't on the base class - it's optional for a
    # standard tech but mandatory for an Assimilator token, so each subclass
    # composes the mixin matching its own cardinality.
    assert not issubclass(TechConfig, CanHaveFactionExclusivity)
    assert not issubclass(TechConfig, RequiresFactionExclusivity)
    assert issubclass(StandardTechConfig, CanHaveFactionExclusivity)
    assert issubclass(AssimilatorTechConfig, RequiresFactionExclusivity)
    # Exhaustible is only meaningful for a real, in-play tech card - an
    # Assimilator token is never itself drawn/exhausted.
    assert not issubclass(TechConfig, CanBeExhaustible)
    assert not issubclass(AssimilatorTechConfig, CanBeExhaustible)
    assert issubclass(StandardTechConfig, CanBeExhaustible)
    # FromDictMixin is only on StandardTechConfig - it's the only subclass
    # with fields needing coercion (prereqs, tech_type). An Assimilator
    # token's fields are all already YAML-native primitives.
    assert not issubclass(TechConfig, FromDictMixin)
    assert not issubclass(AssimilatorTechConfig, FromDictMixin)
    assert issubclass(StandardTechConfig, FromDictMixin)

def test_standard_and_assimilator_tech_config_are_both_tech_configs() -> None:
    """Split introduced specifically for Nekro Virus's Valefar Assimilator
    tokens (see TechID) - they aren't a static tech_type, they become
    whatever technology they assimilate."""
    assert issubclass(StandardTechConfig, TechConfig)
    assert issubclass(AssimilatorTechConfig, TechConfig)

def test_only_standard_tech_config_has_a_tech_type_and_prereqs_field() -> None:
    """An Assimilator token isn't upgraded through the tech tree, so it has
    no prerequisites - tech_type and prereqs both live only on StandardTechConfig."""
    import dataclasses

    standard_fields = {f.name for f in dataclasses.fields(StandardTechConfig)}
    assimilator_fields = {f.name for f in dataclasses.fields(AssimilatorTechConfig)}
    assert {"tech_type", "prereqs"} <= standard_fields
    assert not ({"tech_type", "prereqs"} & assimilator_fields)

def test_assimilator_tech_config_adds_only_faction_exclusive_id() -> None:
    """Not a pure pass-through of TechConfig: it adds the (required)
    faction_exclusive_id field from RequiresFactionExclusivity."""
    import dataclasses

    tech_fields = {f.name for f in dataclasses.fields(TechConfig)}
    assimilator_fields = {f.name for f in dataclasses.fields(AssimilatorTechConfig)}
    assert assimilator_fields - tech_fields == {"faction_exclusive_id"}

def test_construction_of_a_standard_tech() -> None:
    tech = StandardTechConfig(id="x", name="X", functional_text="...", tech_type=TechType.BIOTIC)
    assert tech.tech_type is TechType.BIOTIC

def test_construction_of_an_assimilator_tech_needs_no_tech_type_or_prereqs() -> None:
    tech = AssimilatorTechConfig(
        id="valefar_assimilator_x", name="Valefar Assimilator X", functional_text="...",
        faction_exclusive_id="nekro_virus",
    )
    assert not hasattr(tech, "tech_type")
    assert not hasattr(tech, "prereqs")

def test_assimilator_tech_config_requires_faction_exclusive_id() -> None:
    """Unlike a standard tech's optional exclusivity, Valefar Assimilator
    tokens are only ever printed for Nekro Virus - faction_exclusive_id is
    narrowed to required on this subclass."""
    with pytest.raises(TypeError):
        AssimilatorTechConfig(id="valefar_assimilator_x", name="Valefar Assimilator X", functional_text="...")

def test_standard_tech_from_dict_coerces_tech_type_and_prereqs() -> None:
    from app.config.objs.tech import TechUpgradeReqConfig
    tech = StandardTechConfig.from_dict({
        "id": "x", "name": "X", "functional_text": "...", "tech_type": "warfare",
        "prereqs": [{"tech_type": "biotic", "num": 1}],
    })
    assert tech.tech_type is TechType.WARFARE
    assert tech.prereqs == (TechUpgradeReqConfig(tech_type=TechType.BIOTIC, num=1),)

def test_assimilator_tech_config_has_no_from_dict() -> None:
    """Every AssimilatorTechConfig field (id, name, functional_text,
    faction_exclusive_id) is already a YAML-native primitive - no coercion
    is needed, so it doesn't compose FromDictMixin and has no from_dict."""
    assert not hasattr(AssimilatorTechConfig, "from_dict")
