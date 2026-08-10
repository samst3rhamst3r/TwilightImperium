"""Mirrors src/app/config/yaml_loader.py.

Exercises each per-type loader function individually against the real data/
tree, so a bad field on one Config class fails only that loader's test
instead of cascading into every test that depends on a fully-loaded
RulesetConfig (which composes all of them via a single RulesetConfig.load()
call).
"""
import pytest

from app.config import yaml_loader
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
from app.config.setup import SetupConfig

_LOADER_TO_EXPECTED_TYPE = {
    yaml_loader.load_ability_data: AbilityConfig,
    yaml_loader.load_action_card_data: ActionCardConfig,
    yaml_loader.load_agenda_data: AgendaConfig,
    yaml_loader.load_faction_data: FactionConfig,
    yaml_loader.load_map_data: MapConfig,
    yaml_loader.load_objective_data: ObjectiveConfig,
    yaml_loader.load_planet_data: PlanetConfig,
    yaml_loader.load_promissory_note_data: PromissoryNoteConfig,
    yaml_loader.load_setup_data: SetupConfig,
    yaml_loader.load_strategy_card_data: StrategyCardConfig,
    yaml_loader.load_system_data: SystemConfig,
    yaml_loader.load_tech_data: TechConfig,
    yaml_loader.load_unit_data: UnitConfig,
}

@pytest.mark.parametrize(
    "loader_fn, expected_type", _LOADER_TO_EXPECTED_TYPE.items(), ids=[fn.__name__ for fn in _LOADER_TO_EXPECTED_TYPE]
)
def test_loader_imports_every_real_data_entry_into_the_right_type(
    data_dir, loader_fn, expected_type: type
) -> None:
    items = list(loader_fn(data_dir))
    assert len(items) > 0, f"{loader_fn.__name__} loaded zero entries from data/"
    for item in items:
        assert isinstance(item, expected_type)

def test_every_loaded_id_is_unique_within_its_type(data_dir) -> None:
    for loader_fn in _LOADER_TO_EXPECTED_TYPE:
        ids = [item.id for item in loader_fn(data_dir)]
        duplicates = {id_ for id_ in ids if ids.count(id_) > 1}
        assert not duplicates, f"{loader_fn.__name__} produced duplicate ids: {duplicates}"

def test_text_data_is_merged_by_id_not_left_as_a_separate_lookup(data_dir) -> None:
    """Spot check that _load_text_data_into_config_by_id actually merged the
    flavor/functional text fields onto the config objects it returns, rather
    than the merge silently doing nothing."""
    abilities = list(yaml_loader.load_ability_data(data_dir))
    assert any(ability.functional_text for ability in abilities)
