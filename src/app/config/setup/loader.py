from collections.abc import Generator
from pathlib import Path

from app.config.shared.loader import load_data, SETUP_CONFIG_DATA_PATH
from .base import SetupConfig

def load_setup_data(root_data_path: Path) -> Generator[SetupConfig]:
    for config in load_data(root_data_path / SETUP_CONFIG_DATA_PATH / "setup.yaml"):
        yield SetupConfig.from_dict(config)

def load_first_game_system_tile_mapping(root_data_path: Path, num_players: int) -> tuple[str | None]:
    return tuple(
        load_data(root_data_path / SETUP_CONFIG_DATA_PATH / "first_game_system_tile_mapping" / f"{num_players}_player.yaml")
    )
