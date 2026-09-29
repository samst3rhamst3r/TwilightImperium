"""Mirrors src/app/config/objs/promissory_note/loader.py."""
from types import MappingProxyType

from app.config.objs.promissory_note import (
    FactionPromissoryNoteConfig,
    PromissoryNoteConfig,
    StandardPromissoryNoteConfig,
    load_promissory_note_data,
)

def test_loads_a_populated_id_keyed_index(data_dir) -> None:
    notes = load_promissory_note_data(data_dir)
    assert isinstance(notes, MappingProxyType)
    assert notes
    for key, note in notes.items():
        assert isinstance(note, PromissoryNoteConfig)
        assert key == note.id

def test_each_source_file_loads_into_its_own_subclass(data_dir) -> None:
    notes = load_promissory_note_data(data_dir)
    assert isinstance(notes["trade_agreement"], StandardPromissoryNoteConfig)
    assert isinstance(notes["military_support"], FactionPromissoryNoteConfig)

def test_faction_note_text_is_merged(data_dir) -> None:
    note = load_promissory_note_data(data_dir)["military_support"]
    assert "Sol player" in note.functional_text
