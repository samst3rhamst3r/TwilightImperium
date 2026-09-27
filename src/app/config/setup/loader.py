from pathlib import Path

from config.yaml_loader import load_data, SETUP_CONFIG_DATA_PATH

from .base import SetupConfig

def load_setup_data(root_data_path: Path, num_players: int) -> SetupConfig:
    data = load_data(root_data_path / SETUP_CONFIG_DATA_PATH / "setup.yaml")
    for item in data:
        obj = SetupConfig.from_dict(item)
        if obj.num_players == num_players:
            return obj

    raise ValueError(f"Invalid number of players: {num_players}")
