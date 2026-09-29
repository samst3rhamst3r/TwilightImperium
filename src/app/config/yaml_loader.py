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
    for path, _, _ in config_data_folder_path.walk():
        if path.is_file(follow_symlinks=False):
            res.extend(load_data(path))

    return res