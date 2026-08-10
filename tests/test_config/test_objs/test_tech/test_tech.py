"""Mirrors src/app/config/objs/tech/tech.py."""
from app.config.objs.tech import AssimilatorTechConfig, StandardTechConfig, TechConfig, TechType
from app.config.shared import CanHaveFactionExclusivity, NamedConfigObj, RequiresFunctionalText
from app.config.shared.mixins import CanBeExhaustible

def test_tech_config_composes_the_expected_mixins() -> None:
    assert issubclass(TechConfig, NamedConfigObj)
    assert issubclass(TechConfig, RequiresFunctionalText)
    assert issubclass(TechConfig, CanHaveFactionExclusivity)
    assert issubclass(TechConfig, CanBeExhaustible)

def test_standard_and_assimilator_tech_config_are_both_tech_configs() -> None:
    """Split introduced specifically for Nekro Virus's Valefar Assimilator
    tokens (see TechID) - they aren't a static tech_type, they become
    whatever technology they assimilate."""
    assert issubclass(StandardTechConfig, TechConfig)
    assert issubclass(AssimilatorTechConfig, TechConfig)

def test_only_standard_tech_config_has_a_tech_type_field() -> None:
    import dataclasses

    standard_fields = {f.name for f in dataclasses.fields(StandardTechConfig)}
    assimilator_fields = {f.name for f in dataclasses.fields(AssimilatorTechConfig)}
    assert "tech_type" in standard_fields
    assert "tech_type" not in assimilator_fields

def test_assimilator_tech_config_is_a_pure_pass_through() -> None:
    import dataclasses

    tech_fields = {f.name for f in dataclasses.fields(TechConfig)}
    assimilator_fields = {f.name for f in dataclasses.fields(AssimilatorTechConfig)}
    assert tech_fields == assimilator_fields

def test_construction_of_a_standard_tech() -> None:
    tech = StandardTechConfig(id="x", name="X", functional_text="...", tech_type=TechType.BIOTIC)
    assert tech.tech_type is TechType.BIOTIC

def test_construction_of_an_assimilator_tech_needs_no_tech_type() -> None:
    tech = AssimilatorTechConfig(id="valefar_assimilator_x", name="Valefar Assimilator X", functional_text="...")
    assert not hasattr(tech, "tech_type")
