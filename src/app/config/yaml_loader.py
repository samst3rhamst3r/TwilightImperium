from yaml import safe_load
from pathlib import Path
from typing import Any, Final

CONFIG_OBJ_DATA_PATH: Final[Path] = Path("objs")
SETUP_CONFIG_DATA_PATH: Final[Path] = Path("setup")

def load_data(config_data_file_path: Path) -> Any:
    with open(config_data_file_path) as f:
        return safe_load(f)
