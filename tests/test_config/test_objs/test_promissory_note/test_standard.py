"""Mirrors src/app/config/objs/promissory_note/standard.py."""
import pytest

from app.config.objs.mixins import RequiresFactionExclusivity, RequiresFunctionalText
from app.config.objs.promissory_note import StandardPromissoryNoteConfig

def _standard_notes(ruleset_config) -> list[StandardPromissoryNoteConfig]:
    return [n for n in ruleset_config.promissory_notes.values() if isinstance(n, StandardPromissoryNoteConfig)]

def test_standard_note_has_no_fixed_functional_text_or_faction() -> None:
    """Its text only exists once an issuing player color is known, so it
    carries text *segments* instead of a finished functional_text."""
    assert not issubclass(StandardPromissoryNoteConfig, RequiresFunctionalText)
    assert not issubclass(StandardPromissoryNoteConfig, RequiresFactionExclusivity)

def test_from_dict_converts_segments_to_a_tuple() -> None:
    note = StandardPromissoryNoteConfig.from_dict(
        {"id": "x", "name": "X", "player_color_functional_text": ["When the", "player acts."]}
    )
    assert note.player_color_functional_text == ("When the", "player acts.")

def test_segments_are_required() -> None:
    with pytest.raises(TypeError):
        StandardPromissoryNoteConfig(id="x", name="X")

def test_real_data_has_the_four_standard_notes(ruleset_config) -> None:
    assert {n.id for n in _standard_notes(ruleset_config)} == {
        "trade_agreement", "political_secret", "ceasefire", "support_for_the_throne",
    }

def test_real_standard_notes_have_somewhere_to_insert_the_color(ruleset_config) -> None:
    """Color is inserted *between* segments, so fewer than 2 segments would
    render the note without ever naming the issuing player."""
    for note in _standard_notes(ruleset_config):
        assert len(note.player_color_functional_text) >= 2, f"{note.id} has no color insertion point"
        assert all(segment.strip() for segment in note.player_color_functional_text), (
            f"{note.id} has an empty text segment"
        )

def test_real_standard_notes_no_longer_use_a_placeholder_string(ruleset_config) -> None:
    for note in _standard_notes(ruleset_config):
        for segment in note.player_color_functional_text:
            assert "__" not in segment, f"{note.id} still contains a placeholder token: {segment!r}"
