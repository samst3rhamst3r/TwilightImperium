from pathlib import Path

from config.yaml_loader import load_data, SETUP_CONFIG_DATA_PATH

from .map import MapConfig
from .shape import MapShape

def load_map_data(root_data_path: Path, shape: MapShape) -> MapConfig:
    return MapConfig.from_dict( load_data(root_data_path / SETUP_CONFIG_DATA_PATH / "map" / f"{shape}.yaml") )

def load_first_game_system_tile_mapping(root_data_path: Path, num_players: int) -> tuple[str | None]:
    return tuple(load_data(root_data_path / SETUP_CONFIG_DATA_PATH / "first_game_system_tile_mapping" / f"{num_players}_player.yaml"))
