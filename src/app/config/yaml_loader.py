from yaml import safe_load
from pathlib import Path
from collections.abc import Generator

from app.config.objs.ability.dispatch import PARAMETERIZED_ABILITY_INSTANCE_REGISTRY
from app.config.objs.faction.starting_unit import FactionStartingUnitConfig
from app.config.objs.map.shape import MapShape
from app.config.objs.tech.upgrade_req import TechUpgradeReqConfig
from app.geometry.coordinate import HexCoordinate

from .objs.ability import AbilityConfig
from .objs.action_card import ActionCardConfig
from .objs.agenda import AgendaConfig
from .objs.faction import FactionConfig
from .objs.map import MapConfig
from .objs.objective import ObjectiveConfig
from .objs.planet import PlanetConfig
from .objs.promissory_note import PromissoryNoteConfig
from .objs.strategy_card import StrategyCardConfig
from .objs.system import SystemConfig
from .objs.tech import AssimilatorTechConfig, StandardTechConfig, TechConfig, TechID
from .objs.unit import UnitConfig

from .setup import PlayerSetupConfig, SetupConfig

_CONFIG_OBJ_DATA_PATH = Path("objs")
_TEXT_CONFIG_OBJ_DATA_PATH = Path("text_objs")

def _load_data(config_data_file_path: Path) -> dict | list[dict]:
    with open(config_data_file_path) as f:
        return safe_load(f)

def _load_config_obj_data(root_path: Path, file_name: str) -> list[dict]:
    return _load_data(root_path / _CONFIG_OBJ_DATA_PATH / file_name)

def _load_text_data_into_config_by_id(root_path: Path, file_name: str, *, text_required: bool = True) -> list[dict]:

    config_data: list[dict] = _load_config_obj_data(root_path, file_name)

    text_config_data = {config.pop("id"): config for config in _load_data(root_path / _TEXT_CONFIG_OBJ_DATA_PATH / file_name)}

    for config_dict in config_data:
        if config_dict["id"] not in text_config_data.keys():
            if text_required:
                raise KeyError(f"Text config ID {config_dict['id']} not found in configuration: {config_dict}")
            continue
        config_dict.update(text_config_data[config_dict["id"]])

    return config_data

def load_ability_data(root_data_path: Path) -> Generator[AbilityConfig]:
    for config in _load_text_data_into_config_by_id(root_data_path, "abilities.yaml"):
        yield AbilityConfig(**config)

def load_action_card_data(root_data_path: Path) -> Generator[ActionCardConfig]:
    for config in _load_text_data_into_config_by_id(root_data_path, "action_cards.yaml"):
        config["flavor_text_options"] = tuple(config["flavor_text_options"])
        yield ActionCardConfig(**config)

def load_agenda_data(root_data_path: Path) -> Generator[AgendaConfig]:
    for config in _load_text_data_into_config_by_id(root_data_path, "agendas.yaml"):
        yield AgendaConfig(**config)

def load_faction_data(root_data_path: Path) -> Generator[FactionConfig]:
    for config in _load_config_obj_data(root_data_path, "factions.yaml"):
        config["starting_tech_ids"] = tuple(config["starting_tech_ids"])
        config["starting_units"] = tuple(FactionStartingUnitConfig(**unit_config) for unit_config in config["starting_units"])
        yield FactionConfig(**config)

def load_map_data(root_data_path: Path) -> Generator[MapConfig]:
    base_path = root_data_path / _CONFIG_OBJ_DATA_PATH / "map"
    for path in base_path.iterdir():
        data: dict = _load_data(path)
        data["tiles"] = tuple(HexCoordinate(*tile_coordinate) for tile_coordinate in data["tiles"])
        yield MapConfig(**data)

def load_setup_data(root_data_path: Path) -> Generator[SetupConfig]:
    for config in _load_data(root_data_path / "setup.yaml"):
        yield SetupConfig(
            map_shape_id = MapShape(config["map_shape_id"]),
            player_setup = tuple(PlayerSetupConfig(
                home_system_coordinates = HexCoordinate(*player_setup["home_system_coordinates"]),
                trade_good_bonus = player_setup.get("trade_good_bonus", 0)
            ) for player_setup in config["player_setup"])
        )

def load_objective_data(root_data_path: Path) -> Generator[ObjectiveConfig]:
    for config in _load_text_data_into_config_by_id(root_data_path, "objectives.yaml"):
        yield ObjectiveConfig(**config)

def load_planet_data(root_data_path: Path) -> Generator[PlanetConfig]:
    for config in _load_text_data_into_config_by_id(root_data_path, "planets.yaml"):
        yield PlanetConfig(**config)

def load_promissory_note_data(root_data_path: Path) -> Generator[PromissoryNoteConfig]:
    for config in _load_text_data_into_config_by_id(root_data_path, "promissory_notes.yaml"):
        yield PromissoryNoteConfig(**config)

def load_strategy_card_data(root_data_path: Path) -> Generator[StrategyCardConfig]:
    for config in _load_text_data_into_config_by_id(root_data_path, "strategy_cards.yaml"):
        yield StrategyCardConfig(**config)

def load_system_data(root_data_path: Path) -> Generator[SystemConfig]:
    for config in _load_config_obj_data(root_data_path, "systems.yaml"):
        yield SystemConfig(**config)

def load_tech_data(root_data_path: Path) -> Generator[TechConfig]:
    for config in _load_text_data_into_config_by_id(root_data_path, "techs.yaml"):
        config["prereqs"] = tuple(TechUpgradeReqConfig(**prereq_config) for prereq_config in config["prereqs"])
        if config["id"] in (TechID.VALEFAR_ASSIMILATOR_X, TechID.VALEFAR_ASSIMILATOR_Y):
            yield AssimilatorTechConfig(**config)
        else:
            yield StandardTechConfig(**config)

def load_unit_data(root_data_path: Path) -> Generator[UnitConfig]:
    for config in _load_text_data_into_config_by_id(root_data_path, "units.yaml", text_required=False):
        config["ability_ids"] = tuple(config.get("ability_ids", ()))
        config["upgrade_reqs"] = tuple(
            TechUpgradeReqConfig(**prereq_config) for prereq_config in config.get("upgrade_reqs", ())
        )
        config["parameterized_abilities"] = tuple(
            PARAMETERIZED_ABILITY_INSTANCE_REGISTRY[ability_config["ability_id"]](
                id=ability_config["ability_id"],
                **{key: value for key, value in ability_config.items() if key != "ability_id"},
            )
            for ability_config in config.get("parameterized_abilities", ())
        )
        yield UnitConfig(**config)
