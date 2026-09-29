from yaml import safe_load
from pathlib import Path
from typing import Any, Final

CONFIG_OBJ_DATA_PATH: Final[Path] = Path("objs")
SETUP_CONFIG_DATA_PATH: Final[Path] = Path("setup")

def load_data(config_data_file_path: Path) -> Any:
    with open(config_data_file_path, encoding="utf-8") as f:
        return safe_load(f)

def load_folder_data(config_data_folder_path: Path) -> list[Any]:
    res = []
    for dirpath, _, filenames in config_data_folder_path.walk():
        for filename in filenames:
            res.extend(load_data(dirpath / filename))

    return res