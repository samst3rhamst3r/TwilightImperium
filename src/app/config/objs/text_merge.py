from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, Final
from copy import deepcopy

from app.config.yaml_loader import load_data, CONFIG_OBJ_DATA_PATH

TEXT_CONFIG_OBJ_DATA_PATH: Final[Path] = Path("text_objs")

def merge_text_by_id(
    config: Iterable[Mapping[str, Any]],
    text_data: Iterable[Mapping[str, Any]],
    *,
    text_required: bool = True,
) -> list[dict]:
    """Merge the text data into the config object by id, returning a new
    list with the merged data. The config object is not modified in place.

    Text entries whose id matches no config entry always raise. Config
    entries with no text entry raise only when ``text_required`` is True."""
    text_by_id = {t["id"]: t for t in text_data}
    config = list(config)

    orphan_text_ids = text_by_id.keys() - {c["id"] for c in config}
    if orphan_text_ids:
        raise KeyError(f"Text data IDs {sorted(orphan_text_ids)} do not match any config ID.")

    res: list[dict] = []
    for c in config:
        t = text_by_id.get(c["id"])
        if t is None:
            if text_required:
                raise KeyError(f"Config ID {c['id']} has no matching text data ID.")
            res.append(deepcopy(dict(c)))
        else:
            res.append(deepcopy(c | t))

    return res

def load_and_merge_text_by_id(root_path: Path, rel_path: Path | str, *, text_required: bool = True) -> list[dict]:
    """Load the config and text data from the given file paths, and merge them by id.
    The text_objs .yaml folder structure must mirror the hierarchy of the base objs hierarchy."""
    config = load_data(root_path / CONFIG_OBJ_DATA_PATH / rel_path)
    text_data = load_data(root_path / TEXT_CONFIG_OBJ_DATA_PATH / rel_path)
    return merge_text_by_id(config, text_data, text_required=text_required)
