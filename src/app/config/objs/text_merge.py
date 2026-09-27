from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, Final
from copy import deepcopy

from config.yaml_loader import load_data, CONFIG_OBJ_DATA_PATH

_TEXT_CONFIG_OBJ_DATA_PATH: Final[Path] = Path("text_objs")

def _merge_text_by_id(config: Iterable[Mapping[str, Any]], text_data: Iterable[Mapping[str, Any]]) -> list[dict]:
    """Merge the text data into the config object by id, returning a new
    list with the merged data. The config object is not modified in place."""
    res: list[dict] = []
    for c, t in zip(sorted(config, key=lambda x: x["id"]), sorted(text_data, key=lambda x: x["id"]), strict=True):
        if c["id"] != t["id"]:
            raise KeyError(f"Config ID {c['id']} does not match text data ID {t['id']}.")
        res.append(deepcopy(c | t))

    return res

def load_and_merge_text_by_id(root_path: Path, rel_path: Path) -> list[dict]:
    f"""Load the config and text data from the given file paths, and merge them by id.
    The {_TEXT_CONFIG_OBJ_DATA_PATH} .yaml folder structure must mirror the hierarchy of the base {CONFIG_OBJ_DATA_PATH} hierarchy."""
    config = load_data(root_path / CONFIG_OBJ_DATA_PATH / rel_path)
    text_data = load_data(root_path / _TEXT_CONFIG_OBJ_DATA_PATH / rel_path)
    return _merge_text_by_id(config, text_data)