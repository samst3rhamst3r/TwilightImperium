"""Mirrors src/app/config/objs/ability/loader.py."""
from types import MappingProxyType

from app.config.objs.ability import (
    AbilityConfig,
    FactionAbilityConfig,
    ParameterizedAbilityConfig,
    load_ability_data,
)
from app.config.yaml_loader import load_data

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    abilities = load_ability_data(data_dir)
    assert isinstance(abilities, MappingProxyType)
    assert abilities
    for key, ability in abilities.items():
        assert isinstance(ability, AbilityConfig)
        assert key == ability.id

def test_each_source_file_loads_into_its_own_subclass(data_dir) -> None:
    """faction.yaml -> FactionAbilityConfig, parameterized.yaml ->
    ParameterizedAbilityConfig, standard.yaml -> plain AbilityConfig."""
    abilities = load_ability_data(data_dir)
    assert isinstance(abilities["ambush"], FactionAbilityConfig)
    assert isinstance(abilities["bombardment"], ParameterizedAbilityConfig)
    assert type(abilities["sustain_damage"]) is AbilityConfig

def test_yaml_anchor_shared_args_load_equal_for_every_alias(data_dir) -> None:
    """anti_fighter_barrage / bombardment / space_cannon all alias one
    `&combat_args` anchor - regression guard for FromDictMixin mutating
    that shared dict in place."""
    abilities = load_ability_data(data_dir)
    args = {abilities[i].instance_args for i in ("anti_fighter_barrage", "bombardment", "space_cannon")}
    assert len(args) == 1

def test_every_entry_in_all_three_source_files_is_loaded(data_dir) -> None:
    """Abilities come from three files merged into one index - nothing may
    be dropped along the way (a cross-file duplicate id would raise in
    index_by_id rather than silently collapse)."""
    raw_count = sum(
        len(load_data(data_dir / "objs" / "abilities" / name))
        for name in ("faction.yaml", "parameterized.yaml", "standard.yaml")
    )
    assert len(load_ability_data(data_dir)) == raw_count
