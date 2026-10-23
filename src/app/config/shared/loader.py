from yaml import safe_load
from pathlib import Path

SETUP_CONFIG_DATA_PATH = Path("setup")

_CONFIG_OBJ_DATA_PATH = Path("objs")
_TEXT_CONFIG_OBJ_DATA_PATH = Path("text_objs")

def load_data(config_data_file_path: Path) -> dict | list[dict]:
    with open(config_data_file_path) as f:
        return safe_load(f)

def load_config_obj_data(root_path: Path, file_name: str) -> list[dict]:
    return load_data(root_path / _CONFIG_OBJ_DATA_PATH / file_name)

def load_text_data_into_config_by_id(root_path: Path, file_name: str, *, text_required: bool = True) -> list[dict]:

    config_data: list[dict] = load_config_obj_data(root_path, file_name)

    text_config_data = {config.pop("id"): config for config in load_data(root_path / _TEXT_CONFIG_OBJ_DATA_PATH / file_name)}

    for config_dict in config_data:
        if config_dict["id"] not in text_config_data.keys():
            if text_required:
                raise KeyError(f"Text config ID {config_dict['id']} not found in configuration: {config_dict}")
            continue
        config_dict.update(text_config_data[config_dict["id"]])

    return config_data
