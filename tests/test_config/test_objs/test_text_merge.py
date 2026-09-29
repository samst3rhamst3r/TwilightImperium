"""Mirrors src/app/config/objs/text_merge.py."""
from pathlib import Path

import pytest

from app.config.objs.text_merge import _merge_text_by_id, load_and_merge_text_by_id

def test_merge_combines_config_and_text_by_id() -> None:
    merged = _merge_text_by_id(
        [{"id": "b", "n": 2}, {"id": "a", "n": 1}],
        [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}],
    )
    assert sorted(merged, key=lambda d: d["id"]) == [
        {"id": "a", "n": 1, "text": "A"},
        {"id": "b", "n": 2, "text": "B"},
    ]

def test_merge_does_not_mutate_its_inputs() -> None:
    config = [{"id": "a", "nested": [1]}]
    text = [{"id": "a", "text": "A"}]
    merged = _merge_text_by_id(config, text)
    merged[0]["nested"].append(2)
    assert config == [{"id": "a", "nested": [1]}]
    assert text == [{"id": "a", "text": "A"}]

def test_missing_text_raises_when_text_is_required() -> None:
    with pytest.raises(KeyError):
        _merge_text_by_id([{"id": "a"}, {"id": "b"}], [{"id": "a", "text": "A"}])

def test_missing_text_is_allowed_when_text_is_optional() -> None:
    merged = _merge_text_by_id([{"id": "a"}, {"id": "b"}], [{"id": "a", "text": "A"}], text_required=False)
    assert {"id": "b"} in merged
    assert {"id": "a", "text": "A"} in merged

@pytest.mark.parametrize("text_required", [True, False])
def test_orphan_text_always_raises(text_required: bool) -> None:
    """Text with no matching config entry is always a data bug (usually a
    typo'd or renamed id), whether or not text is optional for the type."""
    with pytest.raises(KeyError):
        _merge_text_by_id([{"id": "a"}], [{"id": "a"}, {"id": "zzz"}], text_required=text_required)

def test_load_and_merge_reads_mirrored_objs_and_text_objs_paths(data_dir: Path) -> None:
    merged = load_and_merge_text_by_id(data_dir, Path("abilities") / "faction.yaml")
    ambush = next(entry for entry in merged if entry["id"] == "ambush")
    assert ambush["name"] == "Ambush"  # from objs/
    assert ambush["functional_text"]   # from text_objs/
