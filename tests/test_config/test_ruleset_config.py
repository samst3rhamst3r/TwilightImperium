"""Mirrors src/app/config/ruleset_config.py."""
from types import MappingProxyType

import pytest

from app.config.objs.ability import AbilityConfig
from app.config.objs.action_card import ActionCardConfig
from app.config.objs.agenda import AgendaConfig
from app.config.objs.faction import FactionConfig
from app.config.objs.map import MapConfig
from app.config.objs.objective import ObjectiveConfig
from app.config.objs.planet import PlanetConfig
from app.config.objs.promissory_note import PromissoryNoteConfig
from app.config.objs.strategy_card import StrategyCardConfig
from app.config.objs.system import SystemConfig
from app.config.objs.tech import TechConfig
from app.config.objs.unit import UnitConfig
from app.config.ruleset_config import RulesetConfig

# Every RulesetConfig field keyed by id, one entry per real-world thing.
_INDEXED_FIELD_TO_TYPE = {
    "abilities": AbilityConfig,
    "action_cards": ActionCardConfig,
    "agendas": AgendaConfig,
    "factions": FactionConfig,
    "maps": MapConfig,
    "objectives": ObjectiveConfig,
    "planets": PlanetConfig,
    "promissory_notes": PromissoryNoteConfig,
    "strategy_cards": StrategyCardConfig,
    "systems": SystemConfig,
    "techs": TechConfig,
    "units": UnitConfig,
}

def test_load_returns_a_ruleset_config(ruleset_config: RulesetConfig) -> None:
    assert isinstance(ruleset_config, RulesetConfig)

@pytest.mark.parametrize("field_name, expected_type", _INDEXED_FIELD_TO_TYPE.items())
def test_every_index_is_a_populated_mapping_proxy_of_the_right_type(
    ruleset_config: RulesetConfig, field_name: str, expected_type: type
) -> None:
    index = getattr(ruleset_config, field_name)
    assert isinstance(index, MappingProxyType)
    assert len(index) > 0, f"RulesetConfig.{field_name} loaded no data from data/"
    for key, value in index.items():
        assert isinstance(value, expected_type)
        assert key == value.id, f"RulesetConfig.{field_name} is keyed by id - {key!r} maps to id {value.id!r}"

def test_setup_is_a_populated_tuple(ruleset_config: RulesetConfig) -> None:
    """Unlike the other fields, `setup` has no single unique key - the same
    map_shape_id repeats across player-count variants (see data/setup.yaml)
    - so it's a plain tuple rather than an id-keyed mapping."""
    from app.config.setup import SetupConfig

    assert isinstance(ruleset_config.setup, tuple)
    assert len(ruleset_config.setup) > 0
    assert all(isinstance(item, SetupConfig) for item in ruleset_config.setup)

def test_ruleset_config_instance_is_frozen(ruleset_config: RulesetConfig) -> None:
    with pytest.raises((AttributeError, TypeError)):
        ruleset_config.units = MappingProxyType({})

def test_index_mappings_reject_item_assignment(ruleset_config: RulesetConfig) -> None:
    """A MappingProxyType view still reflects mutations to its underlying dict
    unless that dict is never exposed anywhere - this asserts the proxy
    itself refuses direct mutation, which is the guarantee __post_init__ is
    meant to provide."""
    for field_name in _INDEXED_FIELD_TO_TYPE:
        index = getattr(ruleset_config, field_name)
        with pytest.raises(TypeError):
            index["__should_not_be_settable__"] = None

def test_ruleset_config_object_graph_is_frozen_all_the_way_down(
    ruleset_config: RulesetConfig, runtime_mutability_violations
) -> None:
    """The full requirement: not just the top-level indices, but every
    nested collection reachable from RulesetConfig (tuples of sub-configs,
    values inside those tuples, etc.) must be frozen, not just the outer
    MappingProxyType layer."""
    violations = runtime_mutability_violations(ruleset_config)
    assert not violations, "\n".join(violations)
