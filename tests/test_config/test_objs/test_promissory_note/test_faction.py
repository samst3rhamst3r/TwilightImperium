"""Mirrors src/app/config/objs/promissory_note/faction.py."""
from collections import Counter

import pytest

from app.config.objs.mixins import RequiresFactionExclusivity, RequiresFunctionalText
from app.config.objs.promissory_note import FactionPromissoryNoteConfig

def _faction_notes(ruleset_config) -> list[FactionPromissoryNoteConfig]:
    return [n for n in ruleset_config.promissory_notes.values() if isinstance(n, FactionPromissoryNoteConfig)]

def test_faction_note_composes_the_expected_mixins() -> None:
    assert issubclass(FactionPromissoryNoteConfig, RequiresFactionExclusivity)
    assert issubclass(FactionPromissoryNoteConfig, RequiresFunctionalText)

def test_faction_is_required() -> None:
    with pytest.raises(TypeError):
        FactionPromissoryNoteConfig(id="x", name="X", functional_text="...")

def test_real_faction_notes_reference_real_factions(ruleset_config) -> None:
    for note in _faction_notes(ruleset_config):
        assert note.faction_exclusive_id in ruleset_config.factions, (
            f"{note.id} references unknown faction {note.faction_exclusive_id!r}"
        )

def test_every_real_faction_has_exactly_one_faction_note(ruleset_config) -> None:
    counts = Counter(note.faction_exclusive_id for note in _faction_notes(ruleset_config))
    assert set(counts) == set(ruleset_config.factions), (
        f"factions without a note: {sorted(set(ruleset_config.factions) - set(counts))}"
    )
    assert all(n == 1 for n in counts.values()), {f: n for f, n in counts.items() if n != 1}
