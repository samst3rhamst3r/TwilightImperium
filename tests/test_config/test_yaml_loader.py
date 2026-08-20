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
from app.config.objs.tech import AssimilatorTechConfig, StandardTechConfig, TechConfig, TechID
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

# SetupConfig has no `id` field at all - see test_setup_variants_are_unique_by_shape_and_player_count
# below for its own (different-shaped) uniqueness check.
_ID_BASED_LOADERS = {
    fn: expected_type for fn, expected_type in _LOADER_TO_EXPECTED_TYPE.items() if fn is not yaml_loader.load_setup_data
}

@pytest.mark.parametrize("loader_fn", _ID_BASED_LOADERS.keys(), ids=[fn.__name__ for fn in _ID_BASED_LOADERS])
def test_loaded_ids_are_unique_within_their_type(data_dir, loader_fn) -> None:
    ids = [item.id for item in loader_fn(data_dir)]
    duplicates = {id_ for id_ in ids if ids.count(id_) > 1}
    assert not duplicates, f"{loader_fn.__name__} produced duplicate ids: {duplicates}"

def test_setup_variants_are_unique_by_shape_and_player_count(data_dir) -> None:
    """SetupConfig has no id - map_shape_id repeats across player-count
    variants (see data/setup.yaml) - so uniqueness is judged by the
    (map_shape_id, player count) pair instead."""
    setups = list(yaml_loader.load_setup_data(data_dir))
    keys = [(setup.map_shape_id, len(setup.player_setup)) for setup in setups]
    duplicates = {key for key in keys if keys.count(key) > 1}
    assert not duplicates, f"load_setup_data produced duplicate (map_shape_id, player count) variants: {duplicates}"

@pytest.mark.parametrize("num_players", [3, 4, 5, 6])
def test_first_game_system_tile_mapping_length_matches_its_map_shape(
    data_dir, ruleset_config, num_players: int
) -> None:
    """First-Game Setup uses a preset map diagram by player count - 3
    players use the (smaller) triangular map, 4-6 players use the standard
    map - so the mapping's length must match that map's tile count exactly,
    positionally (see MapConfig.tiles, which the mapping is zipped against
    in game_setup_session.py)."""
    map_shape_id = "triangular" if num_players == 3 else "standard"
    expected_length = len(ruleset_config.maps[map_shape_id].tiles)

    mapping = yaml_loader.load_first_game_system_tile_mapping(data_dir, num_players)
    assert len(mapping) == expected_length

@pytest.mark.parametrize("num_players", [3, 4, 5, 6])
def test_first_game_system_tile_mapping_non_null_entries_are_real_system_ids(
    data_dir, ruleset_config, num_players: int
) -> None:
    mapping = yaml_loader.load_first_game_system_tile_mapping(data_dir, num_players)
    non_null = [system_id for system_id in mapping if system_id is not None]
    assert non_null, f"expected at least one placed system in the {num_players}-player mapping"
    for system_id in non_null:
        assert system_id in ruleset_config.systems, (
            f"{num_players}-player first-game mapping references unknown system id {system_id!r}"
        )

@pytest.mark.parametrize("num_players", [3, 4, 5, 6])
def test_first_game_system_tile_mapping_has_no_duplicate_system_placements(
    data_dir, num_players: int
) -> None:
    mapping = yaml_loader.load_first_game_system_tile_mapping(data_dir, num_players)
    non_null = [system_id for system_id in mapping if system_id is not None]
    duplicates = {system_id for system_id in non_null if non_null.count(system_id) > 1}
    assert not duplicates, f"{num_players}-player mapping places the same system twice: {duplicates}"

def test_text_data_is_merged_by_id_not_left_as_a_separate_lookup(data_dir) -> None:
    """Spot check that _load_text_data_into_config_by_id actually merged the
    flavor/functional text fields onto the config objects it returns, rather
    than the merge silently doing nothing."""
    abilities = list(yaml_loader.load_ability_data(data_dir))
    assert any(ability.functional_text for ability in abilities)

def test_unit_text_is_optional_but_still_merged_when_present(data_dir) -> None:
    units = list(yaml_loader.load_unit_data(data_dir))
    assert any(unit.functional_text is None for unit in units), (
        "expected at least one unit with no functional_text (e.g. a basic Cruiser) - "
        "if this fails, the text_required=False path may no longer be exercised by real data"
    )
    assert any(unit.functional_text for unit in units), (
        "expected at least one unit with functional_text actually merged in"
    )

def test_tech_loader_splits_assimilator_ids_into_the_right_subclass(data_dir) -> None:
    techs = {tech.id: tech for tech in yaml_loader.load_tech_data(data_dir)}
    assert isinstance(techs[TechID.VALEFAR_ASSIMILATOR_X], AssimilatorTechConfig)
    assert isinstance(techs[TechID.VALEFAR_ASSIMILATOR_Y], AssimilatorTechConfig)
    non_assimilator_techs = [
        tech for id_, tech in techs.items()
        if id_ not in (TechID.VALEFAR_ASSIMILATOR_X, TechID.VALEFAR_ASSIMILATOR_Y)
    ]
    assert non_assimilator_techs, "expected at least one real (non-assimilator) tech in the data"
    assert all(isinstance(tech, StandardTechConfig) for tech in non_assimilator_techs)
