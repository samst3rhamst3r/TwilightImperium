from yaml import safe_load
from pathlib import Path

SETUP_CONFIG_DATA_PATH = Path("setup")

_CONFIG_OBJ_DATA_PATH = Path("objs")

def load_data(config_data_file_path: Path) -> dict | list[dict]:
    with open(config_data_file_path) as f:
        return safe_load(f)

def load_config_obj_data(root_path: Path, file_name: str) -> list[dict]:
    return load_data(root_path / _CONFIG_OBJ_DATA_PATH / file_name)
